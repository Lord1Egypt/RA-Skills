#!/usr/bin/env python3
"""
Basic usage examples for graph-db-toolkit.
"""
import sys
sys.path.insert(0, "../scripts")

from cypher_builder import CypherBuilder
from graph_analytics import GraphAnalytics

def demo_cypher_builder():
    qb = CypherBuilder()
    qb.match_node("a", "Person", {"name": "Alice"})
    qb.match_path("a", "KNOWS", "b")
    qb.returns("a.name", "b.name")
    print("Generated Cypher:", qb.build())
    print("Parameters:", qb.parameters)

def demo_graph_analytics():
    ga = GraphAnalytics()
    nodes = [{"id": "A"}, {"id": "B"}, {"id": "C"}]
    rels = [{"source": "A", "target": "B"}, {"source": "B", "target": "C"}, {"source": "A", "target": "C"}]
    ga.from_neo4j_results(nodes, rels)
    print("Degree centrality:", ga.degree_centrality())
    print("Shortest path A->C:", ga.shortest_path("A", "C"))

if __name__ == "__main__":
    demo_cypher_builder()
    demo_graph_analytics()
