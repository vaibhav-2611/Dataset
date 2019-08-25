import networkx as nx
import pandas as pd
import collections
import csv,os
import pickle
import datetime, time

def Save_Graph(g, filename):
    N = list(g.nodes())
    N.sort()
    f = open(filename,"w")
    for node in N:
        f.write(str(int(node)))
        edgelist = g.edges(node, data=True)
        for e in edgelist:
            u = str(int(e[0]))
            v = str(int(e[1]))
            w = str(e[2]['weight'])
            assert(u==str(int(node)))
            f.write(" "+v+" "+w)
        f.write("\n")
    print("done")
    f.close()

with open('event_total.pkl', 'rb') as f:
    data = pickle.load(f)

with open('event_total.csv', 'w') as f:
    writer = csv.writer(f , lineterminator='\n')
    for tup in data:
        writer.writerow(tup)


Data = pd.read_csv("event_total.csv",sep=',', header=None)

if not os.path.exists("Relation0"):
    os.mkdir("Relation0")

if not os.path.exists("Relation1"):
    os.mkdir("Relation1")

Nodes = set()
Time  = dict()
for i in range(len(Data)):
    u = Data.iloc[i,0]
    v = Data.iloc[i,1]
    t = Data.iloc[i,2]
    r = Data.iloc[i,3]
    Nodes.add(u)
    Nodes.add(v)
    if(t not in Time):
        Time[t]=list()
    Time[t].append((u,v,r))

N = list(Nodes)
N.sort()
od = collections.OrderedDict(sorted(Time.items()))

###################################################################
baseFolder = "Relation0/"
# Initialising the Graph with all possible nodes
N =list(Nodes)
N.sort()
g = nx.DiGraph()
for i in N:
    g.add_node(i)

# Relation = 0
# Adding new edges to graph for each timestamp
filename = -1
for i in od:
    exist = False
    for edge in od[i]:
        u = edge[0]
        v = edge[1]
        r = edge[2]
        if(r==0):
            exist = True
            if(g.has_edge(u,v)):
                tw = g.get_edge_data(u,v)['weight']
                g.add_edge(u,v, weight=tw+1.0)
                g.add_edge(v,u, weight=tw+1.0)
            else:
                g.add_edge(u,v, weight=1.0)
                g.add_edge(v,u, weight=1.0)        
        else:
            continue
    if(exist):
        filename+=1
        Save_Graph(g,baseFolder+str(filename))
        print("done", filename)
###################################################################

baseFolder = "Relation1/"
# Initialising the Graph with all possible nodes
N =list(Nodes)
N.sort()
g = nx.DiGraph()
for i in N:
    g.add_node(i)

# Relation = 1
# Adding new edges to graph for each timestamp
filename = -1
for i in od:
    exist = False
    for edge in od[i]:
        u = edge[0]
        v = edge[1]
        r = edge[2]
        if(r==1):
            exist = True
            if(g.has_edge(u,v)):
                tw = g.get_edge_data(u,v)['weight']
                g.add_edge(u,v, weight=tw+1.0)
                g.add_edge(v,u, weight=tw+1.0)
            else:
                g.add_edge(u,v, weight=1.0)
                g.add_edge(v,u, weight=1.0)        
        else:
            continue
    if(exist):
        filename+=1
        Save_Graph(g,baseFolder+str(filename))
        print("done", filename)
###################################################################