"""
Graph analytics algorithms using NetworkX fallback.
"""
from typing import Dict, List, Any, Optional
import numpy as np

try:
    import networkx as nx
except ImportError:
    nx = None

class GraphAnalytics:
    def __init__(self):
        self.G = nx.DiGraph() if nx else None

    def from_neo4j_results(self, nodes: List[Dict], relationships: List[Dict]):
        """Load from Neo4j-style results."""
        if self.G is None:
            raise ImportError("networkx not installed")
        for n in nodes:
            nid = n.get("id", n.get("name"))
            self.G.add_node(nid, **n)
        for r in relationships:
            src = r.get("source") or r.get("from")
            tgt = r.get("target") or r.get("to")
            self.G.add_edge(src, tgt, **{k: v for k, v in r.items() if k not in ("source", "target", "from", "to")})

    def degree_centrality(self) -> Dict[str, float]:
        if self.G is None:
            raise ImportError("networkx not installed")
        return nx.degree_centrality(self.G)

    def betweenness_centrality(self) -> Dict[str, float]:
        if self.G is None:
            raise ImportError("networkx not installed")
        return nx.betweenness_centrality(self.G)

    def pagerank(self, alpha: float = 0.85) -> Dict[str, float]:
        if self.G is None:
            raise ImportError("networkx not installed")
        return nx.pagerank(self.G, alpha=alpha)

    def shortest_path(self, source: str, target: str) -> List[str]:
        if self.G is None:
            raise ImportError("networkx not installed")
        try:
            return nx.shortest_path(self.G, source=source, target=target)
        except nx.NetworkXNoPath:
            return []

    def community_louvain(self) -> Dict[str, int]:
        if self.G is None:
            raise ImportError("networkx not installed")
        try:
            import community as community_louvain
            return community_louvain.best_partition(self.G.to_undirected())
        except ImportError:
            # fallback: connected components
            comps = list(nx.connected_components(self.G.to_undirected()))
            membership = {}
            for i, comp in enumerate(comps):
                for node in comp:
                    membership[node] = i
            return membership
