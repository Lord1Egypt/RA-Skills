---
name: graph_path_reasoning_analyzer
title: Graph Path Reasoning Analyzer
description: Analyze and discover paths between entities in knowledge graphs to explain relationships, identify indirect connections, and provide reasoning over traversal patterns. Supports shortest path, all paths, filtering, ranking, and explanation generation.
category: reasoning
tags:
  - knowledge-graph
  - reasoning
  - path-finding
  - graph-analysis
  - relationship-discovery
  - explainability
  - shortest-path
  - multi-hop-reasoning
  - connection-analysis
  - graph-traversal
version: 1.0.0
author: community
license: MIT
metadata:
  {"openclaw":{"emoji":"🧭","homepage":"https://clawhub.com"}}
---

# Graph Path Reasoning Analyzer

**Discover and analyze paths between entities to explain relationships and understand indirect connections in knowledge graphs.**

This skill enables comprehensive path reasoning by traversing graphs to find connections between entities, explaining how they are related through intermediate nodes and relationships, and ranking paths by various metrics.

## Quick Start

### Use When
- Explaining why two entities are connected
- Discovering indirect relationships between nodes
- Analyzing multi-hop connections in networks
- Investigating fraud or anomaly patterns
- Building recommendation chains
- Understanding relationship flows
- Explainability in graph-based systems
- Analyzing network connectivity

### Inputs
- Knowledge graph with nodes and relationships
- Source node (starting entity)
- Target node (destination entity)
- Optional path filtering and ranking parameters
- Optional maximum path length

### Outputs
- Path(s) between source and target
- Distance (number of hops)
- Relationship sequences explaining connections
- Path rankings and statistics
- Natural language explanations
- Path diversity metrics

## Path Reasoning Concepts

### Direct Connection
Two entities connected by a single relationship edge.

```
Alice --WORKS_AT--> Acme
```

### Indirect Connection
Two entities connected through intermediate nodes (multi-hop path).

```
Alice --WORKS_AT--> Acme --PARTNER_OF--> BetaCorp --LOCATED_IN--> California
(Alice is indirectly connected to California)
```

### Shortest Path
The minimum number of hops between two nodes, often the most direct explanation.

```
Distance: 3 hops
Path: Alice → Acme → BetaCorp → California
```

### All Paths
Complete enumeration of all possible connection routes between nodes.

```
Path 1: Alice → Acme → BetaCorp (distance 2)
Path 2: Alice → Acme → Partner1 → BetaCorp (distance 3)
Path 3: Alice → Employee_of_Partner → BetaCorp (distance 2)
```

### Path Diversity
Multiple independent paths connecting entities, indicating robustness or redundancy.

```
Paths found: 5
Diversity: High (multiple independent routes)
Critical edges: 1 (single point of failure edges)
```

### Reasoning Chain
A sequence of relationships explaining entity connections, optimized for explainability.

```
Alice works at Acme
Acme partners with BetaCorp
BetaCorp is located in California

Therefore: Alice is connected to California through her employer's partnership
```

## Graph Traversal Algorithms

### 1. Breadth-First Search (BFS)
- Find shortest path efficiently
- Explores neighbors level-by-level
- Complexity: O(V + E) time

```
BFS finds: Alice → Company → Partner → Location
Distance: 3 hops (shortest)
```

### 2. Depth-First Search (DFS)
- Explore deep paths first
- Useful for finding specific patterns
- Complexity: O(V + E) time

```
DFS explores: Alice → Person1 → Person2 → Company → Location
Distance: 4 hops
```

### 3. Dijkstra's Algorithm
- Shortest path with weighted edges
- Considers edge weights (confidence, strength, cost)
- Complexity: O((V + E) log V)

```
Weighted shortest path:
Alice --(0.9)--> Acme --(0.8)--> BetaCorp
Total weight: 0.72 (confidence product)
```

### 4. K-Shortest Paths
- Find top-K most relevant paths
- Balance between distance and quality
- Complexity: O(K * E log V)

```
Top-3 paths by relevance:
1. Direct path (distance: 2, confidence: 0.95)
2. Alt path A (distance: 3, confidence: 0.85)
3. Alt path B (distance: 3, confidence: 0.80)
```

### 5. All-Pairs Shortest Path
- Compute distances between all node pairs
- Floyd-Warshall algorithm
- Complexity: O(V³) time

```
Precomputed distances for rapid queries
Alice ↔ BetaCorp: 2 hops
Alice ↔ California: 3 hops
```

## Path Analysis Strategies

### Strategy 1: Find Shortest Path
Identify the most direct connection.

```
Query: find_shortest_path("Alice", "California")
Result: Alice → Acme → BetaCorp → California
Distance: 3 hops
```

### Strategy 2: Find All Paths
Discover all possible connections.

```
Query: find_all_paths("Alice", "California", max_length=5)
Result: 4 paths found
  Path 1: Alice → Acme → BetaCorp → California (3 hops)
  Path 2: Alice → Acme → Partner1 → Supplier → California (4 hops)
  Path 3: Alice → Employee_friend → Company → California (3 hops)
  Path 4: Alice → ... → California (4 hops)
```

### Strategy 3: Filtered Path Finding
Find paths with specific relationship types.

```
Query: find_paths_by_types("Alice", "California", types=["works_at", "partner_of"])
Result: Only paths using specified relationships
```

### Strategy 4: Weighted Path Finding
Consider edge properties (confidence, weight, cost).

```
Query: find_best_path("Alice", "California", metric="confidence")
Result: Path with highest cumulative confidence
Confidence: 0.95 * 0.90 * 0.85 = 0.726
```

### Strategy 5: Path Pattern Detection
Identify repeating patterns in paths.

```
Pattern detected: Person → Company → Partner → Location
Frequency: 3 paths match this pattern
Strength: 85% of paths follow this structure
```

## Path Ranking Metrics

### Distance-Based Ranking
Prioritize shorter paths (fewer hops).

```
Path A: 2 hops (score: 1.0)
Path B: 3 hops (score: 0.67)
Path C: 4 hops (score: 0.5)
```

### Confidence-Based Ranking
Score by cumulative relationship confidence.

```
Path A: conf=0.95*0.90 = 0.855 (score: 1.0)
Path B: conf=0.85*0.80*0.75 = 0.510 (score: 0.60)
```

### Diversity-Based Ranking
Prioritize diverse paths using different edges.

```
Path A: Uses edges {e1, e2, e3}
Path B: Uses edges {e4, e5, e6} (different edges)
Diversity score for B: Higher (uses new edges)
```

### Semantic Relevance Ranking
Rank by domain-specific relevance scores.

```
Path A: Directly business-relevant (score: 0.95)
Path B: Indirectly related (score: 0.60)
Rank: Path A first
```

## Path Filtering Techniques

### Relationship Type Filtering
Include/exclude specific relationship types.

```
Include: works_at, partner_of, located_in
Exclude: knows, follows
Result: Only business-relevant paths
```

### Depth Limiting
Restrict maximum path length.

```
Max depth: 4 hops
Paths > 4 hops filtered out
Rationale: Distant connections less relevant
```

### Weight Threshold Filtering
Include only edges above confidence threshold.

```
Min confidence: 0.75
Edges below 0.75 excluded from paths
Result: Only high-confidence paths
```

### Temporal Filtering
Consider time-based properties.

```
Time window: 2020-2023
Exclude relationships outside window
Result: Historically relevant paths only
```

## Path Explanation Generation

### Template-Based Explanation
Convert paths to natural language.

```
Path: Alice → Acme → BetaCorp
Template: "{source} works at {intermediate}. 
           {intermediate} partners with {target}."
Result: "Alice works at Acme. Acme partners with BetaCorp."
```

### Graph Serialization Explanation
Express paths in various formats.

```
Neo4j: MATCH path = (a:Person)-[*3]-(b:Company) RETURN path
SPARQL: ?alice ?p1 ?company . ?company ?p2 ?target .
RDF: alice --works_at--> acme --partner_of--> betacorp
```

### Strength-Based Explanation
Emphasize path quality/strength.

```
"Strong connection (confidence: 85%)"
"Weak connection (confidence: 40%)"
"Multiple independent paths (high redundancy)"
```

## Error Handling

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| No path found | Entities disconnected | Check graph connectivity |
| Too many paths | Highly connected graph | Apply depth limit, filter types |
| Path too long | Distant entities | Increase max_depth or accept distance |
| Low confidence | Weak relationships | Apply confidence threshold |
| Timeout | Complex traversal | Limit depth, use shortest path only |
| Memory overflow | Large result set | Paginate results, use K-shortest |

## Best Practices

✓ **Limit traversal depth** - Prevent exponential growth in large graphs  
✓ **Filter relationship types** - Focus on relevant connections  
✓ **Prioritize shortest paths** - Most direct explanations are clearest  
✓ **Add confidence scores** - Weight relationships by certainty  
✓ **Generate explanations** - Convert paths to human-readable form  
✓ **Cache frequent paths** - Improve performance for repeated queries  
✓ **Detect path patterns** - Understand common connection structures  
✓ **Rank by relevance** - Present most important paths first  
✓ **Handle disconnected nodes** - Return meaningful error messages  
✓ **Monitor performance** - Track path finding latency  

## Advanced Features

### Multi-Target Path Finding
Find paths from source to multiple targets simultaneously.

### Path Clustering
Group similar paths by structure or properties.

### Anomaly Detection
Identify unusual or suspicious path patterns.

### Path Evolution
Track how paths change over time in dynamic graphs.

### Cross-Graph Path Finding
Find paths spanning multiple interconnected graphs.

## Integration Points

This skill integrates with:

- **Causal Chain Analyzer** - Understand causal paths
- **Transitive Closure Generator** - Compute all reachable nodes
- **Graph Rule Engine Builder** - Define path-based rules
- **Multi-Hop Reasoning Query Builder** - Build complex path queries
- **Recommendation Engine** - Path-based recommendations
- **Anomaly Detector** - Detect suspicious path patterns

## Recommended Libraries

### Graph Processing
- `networkx` - Path finding algorithms
- `igraph` - Fast path computation
- `graph-tool` - High-performance graph analysis

### Path Algorithms
- `astar` - A* search implementation
- `heapq` - Priority queue for Dijkstra's
- `collections.deque` - BFS queue

### Data Structures
- `dataclasses` - Configuration and results
- `typing` - Type hints

### Visualization
- `matplotlib` - Plot paths
- `pyvis` - Interactive network visualization
- `plotly` - Graph visualization

## Related Skills

- **Causal Chain Analyzer** - Analyze cause-effect chains
- **Transitive Closure Generator** - Compute reachable nodes
- **Graph Rule Engine Builder** - Define path-based rules
- **Multi-Hop Reasoning Query Builder** - Build complex queries
- **Graph Query Optimization** - Optimize path queries

---

**Version:** 1.0.0
