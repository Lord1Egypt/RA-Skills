# Graph Database Toolkit

Graph database toolkit for Neo4j and Cypher-based operations.

## 功能 | Features

- Neo4j 连接与 CRUD | Neo4j connection and CRUD
- Cypher 查询构建器 | Cypher query builder
- 图算法 | Graph algorithms (centrality, shortest path, community)
- 知识图谱操作 | Knowledge graph operations
- 批量导入 | Batch import utilities

## 安装 | Installation

```bash
pip install -r requirements.txt
```

## 快速开始 | Quick Start

```python
from scripts.neo4j_client import Neo4jClient

client = Neo4jClient(uri="bolt://localhost:7687", user="neo4j", password="password")
client.create_node("Person", {"name": "Alice"})
client.create_relationship("Alice", "Person", "KNOWS", "Bob", "Person")
results = client.query("MATCH (n:Person) RETURN n.name")
```

## 目录结构 | Structure

```
graph-db-toolkit/
├── SKILL.md
├── README.md
├── requirements.txt
├── scripts/
│   ├── neo4j_client.py
│   ├── cypher_builder.py
│   └── graph_analytics.py
├── examples/
│   └── basic_usage.py
└── tests/
    └── test_neo4j_client.py
```
