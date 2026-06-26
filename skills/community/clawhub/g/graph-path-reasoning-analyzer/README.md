# Graph Path Reasoning Analyzer - Quick Reference

Analyze and discover paths between entities in knowledge graphs to explain relationships, identify indirect connections, and provide reasoning over traversal patterns.

## 📁 Structure

```
graph-path-reasoning-analyzer/
│
├── SKILL.md                         # Skill definition & overview
│
├── references/                      # Technical guidance
│   └── graph-path-patterns.md       # Path algorithms & strategies
│
├── examples/                        # Domain examples
│   └── graph-path-examples.md       # Real-world path reasoning scenarios
│
└── scripts/                         # Utility scripts
    └── graph_path_analyzer.py       # GraphPathAnalyzer implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand graph path reasoning fundamentals
2. **Learn:** `references/graph-path-patterns.md` - Path finding algorithms and patterns
3. **See:** `examples/graph-path-examples.md` - Real-world path analysis scenarios

### For Implementation

1. Use `scripts/graph_path_analyzer.py` for path reasoning operations
2. Supports: Path finding, relationship discovery, reasoning chain generation
3. Features: Shortest paths, all paths, filtering, ranking, explanation generation

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, use cases, concepts |
| `graph-path-patterns.md` | Path algorithms, traversal strategies, ranking |
| `graph-path-examples.md` | Business, social, recommendation, investigation examples |
| `graph_path_analyzer.py` | Python GraphPathAnalyzer class |

## ⚡ Key Features

✓ Find shortest paths between entities  
✓ Discover all paths with depth limiting  
✓ Filter paths by relationship types  
✓ Rank paths by multiple metrics  
✓ Generate natural language explanations  
✓ Support weighted edge traversal  
✓ Detect path patterns and anomalies  
✓ Build reasoning chains  
✓ Analyze path statistics and diversity  
✓ Export paths in multiple formats  

## 🧭 Path Reasoning Concepts

### Direct Connection
Two entities connected by a single relationship edge.

### Indirect Connection
Two entities connected through intermediate nodes (multi-hop path).

### Shortest Path
The minimum number of hops between two nodes, often most relevant.

### All Paths
Complete enumeration of all possible connection routes between nodes.

### Path Diversity
Multiple independent paths connecting the same entities, indicating robustness or redundancy.

### Reasoning Chain
A sequence of relationships explaining how entities are connected, useful for explainability.

## 🔗 Usage Example

```python
from scripts.graph_path_analyzer import GraphPathAnalyzer, PathConfig

# Create analyzer with configuration
config = PathConfig(
    graph_data={
        "nodes": {"Alice": {}, "Bob": {}, "Acme": {}, "BetaCorp": {}},
        "edges": [
            {"source": "Alice", "target": "Acme", "type": "works_at"},
            {"source": "Bob", "target": "BetaCorp", "type": "works_at"},
            {"source": "Acme", "target": "BetaCorp", "type": "partner_of"}
        ]
    },
    max_path_length=5,
    find_all_paths=False  # Find shortest path only
)

analyzer = GraphPathAnalyzer(config)

# Find shortest path
path_result = analyzer.find_shortest_path("Alice", "Bob")
print(f"Path: {path_result.path}")
print(f"Distance: {path_result.distance}")
print(f"Explanation: {path_result.explanation}")

# Find all paths
all_paths = analyzer.find_all_paths("Alice", "BetaCorp", max_paths=10)
for path in all_paths:
    print(f"  {path}")

# Analyze path statistics
stats = analyzer.get_path_statistics("Alice", "Bob")
print(f"Path count: {stats['total_paths']}")
print(f"Avg distance: {stats['average_distance']}")
```

## 🧠 Key Concepts

### Path Finding
Discovering connections between nodes using graph traversal algorithms like BFS, DFS, or Dijkstra's.

### Relationship Chains
Sequences of edges forming a reasoning explanation for how entities are connected.

### Path Filtering
Selecting relevant paths based on relationship types, weights, or semantic properties.

### Path Ranking
Prioritizing paths by distance, confidence, strength, or domain-specific criteria.

### Explainability
Converting paths to natural language descriptions of relationships and connections.

## 📖 See Also

- Skill Definition: `SKILL.md`
- Path Algorithms: `references/graph-path-patterns.md`
- Examples: `examples/graph-path-examples.md`
- Implementation: `scripts/graph_path_analyzer.py`

---

**Production-ready modular structure - complete path reasoning toolkit for knowledge graphs.**


