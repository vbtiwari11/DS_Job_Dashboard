import pandas as pd
from dash import dcc,html,Dash,Input,Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

df=pd.read_csv("Data_Science_Jobs_in_India.csv")
fields = ['avg_salary','min_salary','max_salary']
#conversion of salaries into dollars
for field in fields:
  df[field] = (df[field].apply(lambda x: float(x[0:-1]) * 100000) / 78.0).astype(int)

app=Dash(__name__,external_stylesheets=[dbc.themes.CYBORG])

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1("Data Science Jobs Dashboard"),className='text-center text-primary mb-4',width=12),

    ),
    dbc.Row([
        dbc.Col(
            [
                dcc.Dropdown(
                    df.company_name.unique(),
                    id="dp1",
                    value='Capgemini',
                    searchable=True,
                    multi=False,
                    optionHeight=15,
                    search_value='',
                    placeholder='Please Select',
                    clearable=True,),
                dcc.Graph(
                    id="bar1",
                    figure={}
                )
            ],xs=12, sm=12, md=12, lg=5, xl=5,width=5

        ),
        dbc.Col(
            [
                dcc.Dropdown(
                    df.company_name.unique(),
                    id="dp2",
                    value=['Capgemini','TCS'],
                    searchable=True,
                    multi=True,
                    optionHeight=15,
                    search_value='',
                    placeholder='Please Select',
                    clearable=True, ),
                dcc.Dropdown(
                    df.job_title.unique(),
                    id="dp3",
                    value='Data Scientist',
                    searchable=True,
                    optionHeight=15,
                    search_value='',
                    placeholder='Please Select',
                    clearable=True,
                ),
                dcc.Graph(
                    id="hist",
                    figure={}
                )
            ], xs=12, sm=12, md=12, lg=5, xl=5,width=5

        )
    ],justify='around'),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                df.company_name.unique(),
                id="dp4",
                value='Capgemini',
                searchable=True,
                optionHeight=15,
                search_value='',
                placeholder='Please Select',
                clearable=True,
            ),
            dcc.Graph(
                id="Line1",
                figure={}
            )

        ],width=5),
        dbc.Col([
            dcc.Dropdown(
                id="dp5",
                options=[ {'label':'Job_titles','value':'job_title'}],
                value='job_title',
                multi=False,
                clearable=False
            ),
            dcc.Graph(
                id="pie",
                figure={}
            )
        ],width=5)
    ],justify='around')
],fluid=True)



#bar graph1

@app.callback(
    Output(component_id='bar1',component_property='figure'),
    Input(component_id='dp1',component_property='value'),

)
def build_graph(selected_company):
    dff=df[df.company_name==selected_company]
    fig1=px.bar(dff,x='job_title',y=['avg_salary','min_salary','max_salary'],barmode='group')
    fig1.update_layout(legend_title_text="Salary")
    fig1.update_xaxes(title_text="Designation")
    fig1.update_yaxes(title_text="Salaries($)")
    return fig1

#hist1

@app.callback(
    Output(component_id='hist',component_property='figure'),
    Input(component_id='dp2',component_property='value'),
    Input(component_id='dp3',component_property='value')
)
def build2(comp_list,job):
    #dff=df[df.company_name==selected_company1 ]
    dff = df[df['company_name'].isin(comp_list)]
    df1=dff[dff.job_title==job]
    fig2=px.histogram(df1,x='company_name',y='avg_salary')
    fig2.update_xaxes(title_text="Company Names")
    fig2.update_yaxes(title_text="Sum Of AVG Salary($)")
    return fig2


#line1

@app.callback(
    Output(component_id='Line1',component_property='figure'),
    Input(component_id='dp4',component_property='value'),
    #Input(component_id='dp2',component_property='value')
)
def build_line(selected_company1):
    dff=df[df.company_name==selected_company1 ]
    fig3=px.line(dff,x='job_title',y='min_experience')
    #fig.update_layout(legend_title_text="Contestant")
    fig3.update_xaxes(title_text="Designation")
    fig3.update_yaxes(title_text="Experience(years)")
    return fig3

#Pie1

@app.callback(
    Output("pie",'figure'),
    Input("dp5",'value')
)
def build_pie(job):
    dff = df

    piechart=px.pie(
            data_frame=dff,
            names=job,
            title='Job Distribution In India'
            )
    return  piechart








if __name__=='__main__':
    app.run_server(debug=True)


