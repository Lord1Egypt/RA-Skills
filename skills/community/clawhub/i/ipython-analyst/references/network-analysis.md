# Network Analysis Reference

Graph analysis with NetworkX: construction, centrality, community detection, paths, visualization. **Load this reference when the user has graph/network data and wants centrality, communities, shortest paths, or visualization.**

## Setup

```python
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

## Graph Construction

```python
# From edge list (CSV with source, target, [weight] columns)
df = pd.read_csv('/home/z/my-project/upload/edges.csv')
G = nx.from_pandas_edgelist(df, source='source', target='target',
                            edge_attr=['weight'], create_using=nx.Graph)

# From adjacency matrix (numpy)
adj = np.load('/home/z/my-project/upload/adj.npy')
G = nx.from_numpy_array(adj)

# From dict-of-dicts (adjacency list)
adj_dict = {1: {2: {'weight': 0.5}, 3: {'weight': 0.7}}, 2: {3: {'weight': 0.4}}}
G = nx.Graph(adj_dict)

# Directed graph
DG = nx.DiGraph()
DG.add_edges_from([(1, 2), (2, 3), (3, 1)])

# Multi-graph (parallel edges)
MG = nx.MultiGraph()
MG.add_edges_from([(1, 2, {'type': 'follows'}), (1, 2, {'type': 'mentions'})])
```

## Basic Statistics

```python
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print(f"Density: {nx.density(G):.4f}")
print(f"Avg degree: {2 * G.number_of_edges() / G.number_of_nodes():.2f}")
print(f"Clustering coeff: {nx.average_clustering(G):.4f}")
print(f"Transitivity: {nx.transitivity(G):.4f}")
print(f"Connected: {nx.is_connected(G)}")
print(f"Components: {nx.number_connected_components(G)}")
```

## Centrality Measures

```python
degree_cent = nx.degree_centrality(G)         # how many neighbors (normalized)
betweenness = nx.betweenness_centrality(G)    # on how many shortest paths
closeness   = nx.closeness_centrality(G)      # inverse avg distance to all others
eigen       = nx.eigenvector_centrality(G, max_iter=1000)  # influence via neighbors
pagerank    = nx.pagerank(G)

# For weighted graphs, weighted degree = sum of edge weights
weighted_degree = {
    n: sum(d['weight'] for _, _, d in G.edges(n, data=True))
    for n in G.nodes()
}

# Top 5 by each measure
for name, cent in [('degree', degree_cent), ('betweenness', betweenness),
                   ('closeness', closeness), ('eigen', eigen), ('pagerank', pagerank)]:
    top = sorted(cent.items(), key=lambda x: -x[1])[:5]
    print(f"{name:12s}: {top}")
```

## Community Detection

```python
from networkx.algorithms.community import (
    louvain_communities, greedy_modularity_communities, modularity,
)

# Louvain (best for large graphs)
communities = louvain_communities(G, seed=42)
print(f"Found {len(communities)} communities")
print(f"Modularity: {modularity(G, communities):.3f}")

# Map node → community index
node_community = {}
for i, comm in enumerate(communities):
    for node in comm:
        node_community[node] = i

# Greedy modularity (older method, deterministic)
communities_greedy = list(greedy_modularity_communities(G))
```

## Path Analysis

```python
# Shortest path between two nodes
path = nx.shortest_path(G, source=1, target=10, weight='weight')
path_len = nx.shortest_path_length(G, source=1, target=10, weight='weight')

# All shortest paths from one node
lengths = nx.single_source_shortest_path_length(G, source=1)

# Average shortest path length (only for connected graphs)
if nx.is_connected(G):
    avg_path = nx.average_shortest_path_length(G)
    diameter = nx.diameter(G)
    print(f"Avg path length: {avg_path:.3f}, Diameter: {diameter}")

# For disconnected graphs, use the largest component
components = list(nx.connected_components(G))
largest = max(components, key=len)
G_largest = G.subgraph(largest).copy()
print(f"Largest component: {len(largest)} nodes, diameter {nx.diameter(G_largest)}")
```

## Visualization

```python
fig, ax = plt.subplots(figsize=(12, 8), constrained_layout=True)

# Layout — spring is good default; kamada_kawai for small graphs; circular for ring
pos = nx.spring_layout(G, seed=42, k=2 / np.sqrt(G.number_of_nodes()))

# Node size by degree
node_sizes = [300 * (1 + G.degree(n)) for n in G.nodes()]

# Node color by community
colors = [node_community.get(n, 0) for n in G.nodes()]

nx.draw(
    G, pos, ax=ax,
    with_labels=True,
    node_size=node_sizes,
    node_color=colors,
    cmap=plt.cm.Set3,
    edge_color='gray',
    font_size=8,
    alpha=0.85,
)
plt.savefig('/home/z/my-project/download/graph.png', dpi=150)
```

### Layout choice
- `spring_layout` — default, good for most graphs
- `kamada_kawai_layout` — better for small graphs (<100 nodes), preserves edge lengths
- `circular_layout` — for ring structures
- `shell_layout` — for layered/hierarchical
- `spectral_layout` — uses graph Laplacian eigenvectors

## Common Patterns

### Find bridges and articulation points
```python
# Bridges: edges whose removal disconnects the graph
bridges = list(nx.bridges(G))
# Articulation points: nodes whose removal disconnects
articulation = list(nx.articulation_points(G))
print(f"Bridges: {len(bridges)}, Articulation points: {len(articulation)}")
```

### Find cycles
```python
cycles = list(nx.simple_cycles(G)) if G.is_directed() else list(nx.cycle_basis(G))
print(f"Found {len(cycles)} cycles")
```

### Bipartite projection
```python
# If G is bipartite with node attribute 'bipartite'
top_nodes = {n for n, d in G.nodes(data=True) if d.get('bipartite') == 0}
bottom_nodes = set(G) - top_nodes
# Project to bottom nodes (co-occurrence graph)
G_proj = nx.bipartite.weighted_projected_graph(G, bottom_nodes)
```

## Common Pitfalls

### Disconnected graphs
Many centrality measures assume connectivity. `nx.eigenvector_centrality` may not converge on disconnected graphs — try `nx.eigenvector_centrality_numpy` instead.

### Memory on large graphs
`nx.betweenness_centrality(G)` is O(VE) — for >10k nodes, use `nx.betweenness_centrality(G, k=100)` to sample 100 nodes.

### Node ordering
NetworkX doesn't guarantee node order. If you need consistent ordering (e.g., for adjacency matrices), sort: `nodes = sorted(G.nodes())`.

## Output

```python
# Save as GraphML (interoperable with Gephi, Cytoscape)
nx.write_graphml(G, '/home/z/my-project/download/graph.graphml')

# Save centrality as CSV
import pandas as pd
centrality_df = pd.DataFrame({
    'node': list(degree_cent.keys()),
    'degree': list(degree_cent.values()),
    'betweenness': [betweenness[n] for n in degree_cent],
    'closeness': [closeness[n] for n in degree_cent],
    'pagerank': [pagerank[n] for n in degree_cent],
    'community': [node_community.get(n, -1) for n in degree_cent],
})
centrality_df.to_csv('/home/z/my-project/download/centrality.csv', index=False)
```
