---
name: graph-analysis
description: Analyze graphs and networks using Python NetworkX — centrality, shortest paths, community detection, and visualization.
homepage: https://github.com/owenciantar/openclaw-graph-analysis
metadata:
  clawdbot:
    emoji: "🕸️"
    requires:
      env: []
      bin: ["python3", "pip"]
    files: ["scripts/*"]
tags:
  - data-analysis
  - graph-theory
  - networkx
  - visualization
---

# Graph Analysis Skill

Analyze graphs and networks using Python and NetworkX. Supports building graphs from data, running graph algorithms, and generating visualizations.

## Setup

Before first use, install dependencies:

```bash
pip install networkx matplotlib numpy --break-system-packages
```

## Capabilities

### 1. Build a Graph

Create graphs from edge lists, adjacency matrices, CSV files, or JSON data.

**From an edge list (CSV or inline):**
```python
import networkx as nx

# From a CSV file with columns: source, target, weight (optional)
import csv
G = nx.Graph()
with open("edges.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        weight = float(row.get("weight", 1.0))
        G.add_edge(row["source"], row["target"], weight=weight)
```

**From inline data:**
```python
import networkx as nx
G = nx.Graph()
G.add_edges_from([("A", "B"), ("B", "C"), ("A", "C"), ("C", "D")])
```

**Directed graph:**
```python
G = nx.DiGraph()
G.add_edges_from([("A", "B"), ("B", "C")])
```

### 2. Graph Metrics

Run these to answer questions about graph structure:

```python
import networkx as nx

# Basic stats
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print(f"Density: {nx.density(G):.4f}")
print(f"Connected: {nx.is_connected(G)}")

# Centrality measures
degree_cent = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G)
closeness = nx.closeness_centrality(G)
pagerank = nx.pagerank(G)

# Find most important nodes
top_by_degree = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:10]
top_by_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]
top_by_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]

print("Top nodes by degree centrality:", top_by_degree)
print("Top nodes by betweenness:", top_by_betweenness)
print("Top nodes by PageRank:", top_by_pagerank)
```

### 3. Shortest Paths

```python
# Shortest path between two nodes
path = nx.shortest_path(G, source="A", target="D")
length = nx.shortest_path_length(G, source="A", target="D")
print(f"Path: {' -> '.join(path)} (length: {length})")

# Weighted shortest path
path_w = nx.shortest_path(G, source="A", target="D", weight="weight")

# All pairs shortest path lengths
all_lengths = dict(nx.all_pairs_shortest_path_length(G))
```

### 4. Community Detection

```python
from networkx.algorithms.community import greedy_modularity_communities, louvain_communities

# Greedy modularity
communities_greedy = list(greedy_modularity_communities(G))
print(f"Found {len(communities_greedy)} communities (greedy)")

# Louvain (better for large graphs)
communities_louvain = list(louvain_communities(G))
print(f"Found {len(communities_louvain)} communities (Louvain)")

# Print community membership
for i, comm in enumerate(communities_louvain):
    print(f"  Community {i}: {sorted(comm)}")
```

### 5. Visualization

Save graph visualizations as PNG images:

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

fig, ax = plt.subplots(figsize=(12, 8))

# Layout options: spring_layout, circular_layout, kamada_kawai_layout, shell_layout
pos = nx.spring_layout(G, seed=42)

# Size nodes by degree
node_sizes = [300 * G.degree(n) for n in G.nodes()]

# Color nodes by community (if communities were computed)
nx.draw(
    G, pos, ax=ax,
    with_labels=True,
    node_size=node_sizes,
    node_color="steelblue",
    edge_color="#cccccc",
    font_size=8,
    font_weight="bold",
    width=0.8,
)
ax.set_title("Graph Visualization")
plt.tight_layout()
plt.savefig("graph.png", dpi=150)
plt.close()
print("Saved graph.png")
```

**Color by community:**
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community import louvain_communities

communities = list(louvain_communities(G))
color_map = {}
for i, comm in enumerate(communities):
    for node in comm:
        color_map[node] = i

node_colors = [color_map[n] for n in G.nodes()]
pos = nx.spring_layout(G, seed=42)

fig, ax = plt.subplots(figsize=(12, 8))
nx.draw(
    G, pos, ax=ax,
    with_labels=True,
    node_color=node_colors,
    cmap=plt.cm.Set3,
    node_size=500,
    edge_color="#cccccc",
    font_size=8,
)
ax.set_title("Communities")
plt.tight_layout()
plt.savefig("communities.png", dpi=150)
plt.close()
print("Saved communities.png")
```

### 6. Graph Generators (for testing or simulation)

```python
import networkx as nx

# Common test graphs
G = nx.karate_club_graph()          # Classic social network (34 nodes)
G = nx.barabasi_albert_graph(100, 3) # Scale-free network
G = nx.erdos_renyi_graph(50, 0.1)    # Random graph
G = nx.watts_strogatz_graph(30, 4, 0.3)  # Small-world network
```

## When to Use This Skill

Use this skill when the user asks to:
- Analyze relationships, connections, or networks in data
- Find important/central/influential nodes in a network
- Detect communities or clusters in a graph
- Find shortest paths between entities
- Visualize a network or relationship diagram
- Build a graph from CSV, JSON, or other structured data
- Run graph algorithms (PageRank, centrality, clustering coefficient, etc.)

## Notes

- For large graphs (>10,000 nodes), prefer `louvain_communities` over `greedy_modularity_communities`
- Always use `matplotlib.use("Agg")` before importing pyplot (no display server)
- Save visualizations as PNG files and show them to the user
- When reading user data, infer source/target columns from context — common patterns include: from/to, source/target, node1/node2, parent/child
