"""Common graph engine for coupling analysis."""

from typing import Dict, List, Set, Tuple
from collections import defaultdict


class ImportGraph:
    """Represents module dependencies in a codebase."""

    def __init__(self):
        self.nodes: Set[str] = set()
        self.edges: List[Tuple[str, str]] = []  # (importer, imported)
        self.module_to_file: Dict[str, str] = {}  # Map module name to file path

    def add_edge(self, importer: str, imported: str):
        self.nodes.add(importer)
        self.nodes.add(imported)
        self.edges.append((importer, imported))

    def get_afferent_coupling(self, module: str) -> int:
        """Number of modules that import this module (incoming edges)."""
        return sum(1 for src, dst in self.edges if dst == module)

    def get_efferent_coupling(self, module: str) -> int:
        """Number of modules this module imports (outgoing edges)."""
        return sum(1 for src, dst in self.edges if src == module)

    def get_instability(self, module: str) -> float:
        """Instability = efferent / (afferent + efferent). 0=stable, 1=unstable."""
        ca = self.get_afferent_coupling(module)
        ce = self.get_efferent_coupling(module)
        total = ca + ce
        return ce / total if total > 0 else 0.0

    def detect_circular_dependencies(self) -> List[List[str]]:
        """Find cycles in the import graph."""
        # Build adjacency list
        graph = defaultdict(list)
        for src, dst in self.edges:
            graph[src].append(dst)

        # DFS to detect cycles
        visited = set()
        stack = []
        cycles = []

        def dfs(node):
            if node in stack:
                # Cycle detected: from node back to itself in current path
                cycle_start = stack.index(node)
                cycle = stack[cycle_start:] + [node]
                cycles.append(cycle)
                return
            if node in visited:
                return
            visited.add(node)
            stack.append(node)
            for neighbor in graph.get(node, []):
                dfs(neighbor)
            stack.pop()

        for node in sorted(list(self.nodes)): # Sorted for deterministic results
            dfs(node)

        return cycles
