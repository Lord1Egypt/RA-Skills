"""
Unit tests for graph-db-toolkit.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../scripts"))

import unittest
from cypher_builder import CypherBuilder
from graph_analytics import GraphAnalytics

class TestCypherBuilder(unittest.TestCase):
    def test_simple_match(self):
        qb = CypherBuilder()
        qb.match_node("n", "Person", {"name": "Alice"})
        qb.returns("n.name")
        self.assertIn("MATCH", qb.build())
        self.assertIn("Person", qb.build())
        self.assertEqual(qb.parameters["n_name"], "Alice")

    def test_path_match(self):
        qb = CypherBuilder()
        qb.match_path("a", "KNOWS", "b")
        cypher = qb.build()
        self.assertIn("(a)-[:KNOWS]->(b)", cypher)

    def test_shortest_path(self):
        cypher = CypherBuilder.shortest_path("Person", "name", "Alice", "Person", "name", "Bob", max_hops=3)
        self.assertIn("shortestPath", cypher)
        self.assertIn("$start_val", cypher)
        self.assertIn("$end_val", cypher)

class TestGraphAnalytics(unittest.TestCase):
    def test_centrality(self):
        ga = GraphAnalytics()
        nodes = [{"id": "A"}, {"id": "B"}, {"id": "C"}]
        rels = [{"source": "A", "target": "B"}, {"source": "B", "target": "C"}]
        ga.from_neo4j_results(nodes, rels)
        cent = ga.degree_centrality()
        self.assertIn("A", cent)
        self.assertIn("B", cent)

    def test_shortest_path(self):
        ga = GraphAnalytics()
        nodes = [{"id": "A"}, {"id": "B"}, {"id": "C"}]
        rels = [{"source": "A", "target": "B"}, {"source": "B", "target": "C"}]
        ga.from_neo4j_results(nodes, rels)
        path = ga.shortest_path("A", "C")
        self.assertEqual(path, ["A", "B", "C"])

if __name__ == "__main__":
    unittest.main()
