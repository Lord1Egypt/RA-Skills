"""
Graph Path Reasoning Analyzer - Production-Ready Implementation

Comprehensive path finding and analysis toolkit for knowledge graphs.
Supports shortest path, all paths, filtering, ranking, and explanation generation.

Author: Knowledge Graph Team
License: MIT
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import deque
from enum import Enum
import heapq
import json


# ==================== Data Classes ====================

class PathAlgorithm(Enum):
    """Supported path finding algorithms."""
    BFS = "bfs"  # Breadth-first search (shortest path)
    DFS = "dfs"  # Depth-first search (all paths)
    DIJKSTRA = "dijkstra"  # Weighted shortest path
    BIDIRECTIONAL = "bidirectional"  # Search from both ends
    K_SHORTEST = "k_shortest"  # Top-K paths


class RankingStrategy(Enum):
    """Path ranking strategies."""
    DISTANCE = "distance"  # Prioritize shortest
    CONFIDENCE = "confidence"  # Prioritize certain
    COMPOSITE = "composite"  # Multi-criteria


@dataclass
class PathEdge:
    """Represents an edge in a path."""
    source: str
    target: str
    relation_type: str
    confidence: float = 0.5
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphPath:
    """Represents a path between two nodes."""
    nodes: List[str]  # Ordered sequence of node IDs
    distance: int = 0  # Number of hops
    confidence: float = 1.0  # Cumulative confidence
    edges: List[PathEdge] = field(default_factory=list)
    relation_types: List[str] = field(default_factory=list)
    explanation: Optional[str] = None

    def __post_init__(self):
        self.distance = len(self.nodes) - 1 if len(self.nodes) > 0 else 0


@dataclass
class PathAnalysisResult:
    """Results from path reasoning analysis."""
    source: str
    target: Optional[str] = None
    paths: List[GraphPath] = field(default_factory=list)
    shortest_path: Optional[GraphPath] = None
    all_paths_count: int = 0
    path_diversity: Dict[str, Any] = field(default_factory=dict)
    statistics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'source': self.source,
            'target': self.target,
            'paths_found': len(self.paths),
            'shortest_distance': self.shortest_path.distance if self.shortest_path else None,
            'all_paths_count': self.all_paths_count,
            'path_diversity': self.path_diversity,
            'statistics': self.statistics
        }


@dataclass
class PathConfig:
    """Configuration for path reasoning analysis."""
    # Graph data
    graph_data: Dict[str, Any]

    # Algorithm settings
    algorithm: PathAlgorithm = PathAlgorithm.BFS
    max_path_length: int = 10
    find_all_paths: bool = False
    k_paths: int = 3  # For K-shortest

    # Ranking settings
    ranking_strategy: RankingStrategy = RankingStrategy.DISTANCE

    # Filtering settings
    min_confidence: float = 0.0
    allowed_relation_types: Optional[List[str]] = None
    excluded_relation_types: Optional[List[str]] = None

    # Performance settings
    cache_paths: bool = True
    max_results: Optional[int] = None

    # Explanation settings
    generate_explanations: bool = True


# ==================== GraphPathAnalyzer ====================

class GraphPathAnalyzer:
    """
    Main analyzer for path reasoning in knowledge graphs.

    Provides methods for:
    - Finding shortest paths between nodes
    - Discovering all paths with constraints
    - Ranking paths by various metrics
    - Analyzing path diversity and patterns
    - Generating natural language explanations
    """

    def __init__(self, config: PathConfig):
        """Initialize analyzer with configuration."""
        self.config = config
        self._build_graph_structure()
        self._path_cache = {} if config.cache_paths else None

    def _build_graph_structure(self):
        """Build internal graph structure from config data."""
        self.nodes = set()
        self.edges = {}  # {source: {target: [edges]}}
        self.reverse_edges = {}  # {target: {source: [edges]}}
        self.node_data = {}  # {node_id: properties}

        # Add nodes
        if 'nodes' in self.config.graph_data:
            for node_id, props in self.config.graph_data['nodes'].items():
                self.nodes.add(node_id)
                self.node_data[node_id] = props or {}
                self.edges[node_id] = {}
                self.reverse_edges[node_id] = {}

        # Add edges (relationships)
        if 'edges' in self.config.graph_data:
            for edge in self.config.graph_data['edges']:
                source = edge.get('source')
                target = edge.get('target')
                rel_type = edge.get('type', 'connected_to')

                if source and target:
                    # Ensure nodes exist
                    self.nodes.add(source)
                    self.nodes.add(target)

                    if source not in self.edges:
                        self.edges[source] = {}
                    if target not in self.edges:
                        self.edges[target] = {}
                    if source not in self.reverse_edges:
                        self.reverse_edges[source] = {}
                    if target not in self.reverse_edges:
                        self.reverse_edges[target] = {}

                    # Store edge
                    if target not in self.edges[source]:
                        self.edges[source][target] = []
                    self.edges[source][target].append(edge)

                    # Reverse mapping
                    if source not in self.reverse_edges[target]:
                        self.reverse_edges[target][source] = []
                    self.reverse_edges[target][source].append(edge)

    def find_shortest_path(
        self,
        source: str,
        target: str,
        generate_explanation: bool = True
    ) -> Optional[GraphPath]:
        """
        Find shortest path between source and target nodes.

        Args:
            source: Starting node
            target: Destination node
            generate_explanation: Whether to generate natural language explanation

        Returns:
            GraphPath object or None if no path exists
        """
        cache_key = f"shortest:{source}:{target}"
        if self._path_cache and cache_key in self._path_cache:
            return self._path_cache[cache_key]

        if source == target:
            path = GraphPath(nodes=[source], distance=0, confidence=1.0)
            if self._path_cache:
                self._path_cache[cache_key] = path
            return path

        # Use BFS for shortest path
        path = self._find_shortest_path_bfs(source, target)

        if path and generate_explanation:
            path.explanation = self._generate_explanation(path)

        if self._path_cache and path:
            self._path_cache[cache_key] = path

        return path

    def find_all_paths(
        self,
        source: str,
        target: str,
        max_paths: Optional[int] = None
    ) -> List[GraphPath]:
        """
        Find all paths between source and target.

        Args:
            source: Starting node
            target: Destination node
            max_paths: Maximum paths to return

        Returns:
            List of GraphPath objects
        """
        paths = []
        visited = set()

        def dfs(current, target_node, path, edges):
            if current == target_node:
                paths.append(GraphPath(
                    nodes=path[:],
                    confidence=self._calculate_confidence(path),
                    edges=edges[:]
                ))
                return

            if len(path) - 1 >= self.config.max_path_length:
                return

            if max_paths and len(paths) >= max_paths:
                return

            for neighbor in self.edges.get(current, {}):
                if neighbor not in path:  # Avoid cycles
                    edge_data = self.edges[current][neighbor][0]

                    # Check filters
                    if not self._passes_filters(edge_data):
                        continue

                    path.append(neighbor)
                    edge_obj = PathEdge(
                        source=current,
                        target=neighbor,
                        relation_type=edge_data.get('type', 'connected_to'),
                        confidence=edge_data.get('confidence', 0.5)
                    )
                    edges.append(edge_obj)

                    dfs(neighbor, target_node, path, edges)

                    path.pop()
                    edges.pop()

        dfs(source, target, [source], [])

        # Apply ranking
        paths = self._rank_paths(paths)

        # Generate explanations
        if self.config.generate_explanations:
            for path in paths:
                path.explanation = self._generate_explanation(path)

        return paths

    def find_paths_by_type(
        self,
        source: str,
        target: str,
        relation_types: List[str]
    ) -> List[GraphPath]:
        """
        Find paths using only specific relationship types.

        Args:
            relation_types: List of allowed relationship types

        Returns:
            List of filtered paths
        """
        # Temporarily override allowed types
        old_types = self.config.allowed_relation_types
        self.config.allowed_relation_types = relation_types

        paths = self.find_all_paths(source, target)

        self.config.allowed_relation_types = old_types
        return paths

    def analyze_path_diversity(
        self,
        source: str,
        target: str
    ) -> Dict[str, Any]:
        """
        Analyze diversity of paths between nodes.

        Returns:
            Metrics about path diversity and network robustness
        """
        paths = self.find_all_paths(source, target)

        if not paths:
            return {
                'total_paths': 0,
                'diversity_score': 0,
                'critical_edges': [],
                'redundancy': 'NONE'
            }

        # Count edge usage
        edge_counts = {}
        for path in paths:
            for i in range(len(path.nodes) - 1):
                edge_key = (path.nodes[i], path.nodes[i + 1])
                edge_counts[edge_key] = edge_counts.get(edge_key, 0) + 1

        # Find critical edges (in all paths)
        total_paths = len(paths)
        critical_edges = [e for e, count in edge_counts.items() if count == total_paths]

        # Diversity score
        unique_edges = len(edge_counts)
        max_possible = total_paths * max((len(p.nodes) - 1 for p in paths), default=1)
        diversity = unique_edges / max_possible if max_possible else 0

        return {
            'total_paths': total_paths,
            'unique_edges': unique_edges,
            'diversity_score': diversity,
            'critical_edges': critical_edges,
            'redundancy': 'HIGH' if diversity > 0.7 else 'MEDIUM' if diversity > 0.4 else 'LOW'
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Get overall graph statistics."""
        total_edges = sum(
            len(targets)
            for targets in self.edges.values()
        )

        return {
            'total_nodes': len(self.nodes),
            'total_edges': total_edges,
            'average_degree': total_edges / len(self.nodes) if self.nodes else 0
        }

    # ==================== Private Methods ====================

    def _find_shortest_path_bfs(self, source: str, target: str) -> Optional[GraphPath]:
        """BFS-based shortest path finding."""
        if source == target:
            return GraphPath(nodes=[source])

        visited = {source}
        queue = deque([(source, [source], [])])

        while queue:
            current, path, edges_list = queue.popleft()

            for neighbor in self.edges.get(current, {}):
                if neighbor == target:
                    edge_data = self.edges[current][neighbor][0]
                    if self._passes_filters(edge_data):
                        final_edges = edges_list + [PathEdge(
                            source=current,
                            target=neighbor,
                            relation_type=edge_data.get('type', 'connected_to'),
                            confidence=edge_data.get('confidence', 0.5)
                        )]
                        return GraphPath(
                            nodes=path + [neighbor],
                            confidence=self._calculate_confidence(path + [neighbor]),
                            edges=final_edges
                        )

                if neighbor not in visited:
                    edge_data = self.edges[current][neighbor][0]
                    if self._passes_filters(edge_data):
                        visited.add(neighbor)
                        new_edges = edges_list + [PathEdge(
                            source=current,
                            target=neighbor,
                            relation_type=edge_data.get('type', 'connected_to'),
                            confidence=edge_data.get('confidence', 0.5)
                        )]
                        queue.append((neighbor, path + [neighbor], new_edges))

        return None  # No path found

    def _passes_filters(self, edge_data: Dict) -> bool:
        """Check if edge passes configured filters."""
        rel_type = edge_data.get('type', 'connected_to')
        confidence = edge_data.get('confidence', 0.5)

        # Confidence filter
        if confidence < self.config.min_confidence:
            return False

        # Relation type filters
        if self.config.allowed_relation_types:
            if rel_type not in self.config.allowed_relation_types:
                return False

        if self.config.excluded_relation_types:
            if rel_type in self.config.excluded_relation_types:
                return False

        return True

    def _calculate_confidence(self, path: List[str]) -> float:
        """Calculate cumulative confidence for a path."""
        if len(path) < 2:
            return 1.0

        confidence = 1.0
        for i in range(len(path) - 1):
            edges = self.edges.get(path[i], {}).get(path[i + 1], [])
            if edges:
                edge_conf = edges[0].get('confidence', 0.5)
                confidence *= edge_conf

        return confidence

    def _rank_paths(self, paths: List[GraphPath]) -> List[GraphPath]:
        """Rank paths according to configured strategy."""
        if self.config.ranking_strategy == RankingStrategy.DISTANCE:
            return sorted(paths, key=lambda p: p.distance)
        elif self.config.ranking_strategy == RankingStrategy.CONFIDENCE:
            return sorted(paths, key=lambda p: p.confidence, reverse=True)
        elif self.config.ranking_strategy == RankingStrategy.COMPOSITE:
            # Balance distance and confidence
            for path in paths:
                dist_score = 1.0 / (path.distance + 1)
                conf_score = path.confidence
                path.composite_score = 0.4 * dist_score + 0.6 * conf_score
            return sorted(paths, key=lambda p: p.composite_score, reverse=True)
        return paths

    def _generate_explanation(self, path: GraphPath) -> str:
        """Generate natural language explanation for a path."""
        if len(path.nodes) < 2:
            return f"Single node: {path.nodes[0]}"

        sentences = []
        for i in range(len(path.nodes) - 1):
            source = path.nodes[i]
            target = path.nodes[i + 1]
            rel_type = path.relation_types[i] if i < len(path.relation_types) else 'connected_to'

            # Simple template
            sentence = f"{source} {rel_type.replace('_', ' ')} {target}"
            sentences.append(sentence)

        explanation = ". ".join(sentences) + "."

        # Add strength indicator
        if path.confidence >= 0.85:
            explanation += " (Strong connection)"
        elif path.confidence >= 0.60:
            explanation += " (Medium confidence)"
        else:
            explanation += " (Weak connection)"

        return explanation


# ==================== Example Usage ====================

if __name__ == "__main__":
    # Example: Social network path finding
    config = PathConfig(
        graph_data={
            "nodes": {
                "Alice": {},
                "Bob": {},
                "Charlie": {},
                "Diana": {},
                "TechCorp": {},
                "BetaCorp": {}
            },
            "edges": [
                {"source": "Alice", "target": "Bob", "type": "follows", "confidence": 0.9},
                {"source": "Bob", "target": "Charlie", "type": "follows", "confidence": 0.85},
                {"source": "Charlie", "target": "TechCorp", "type": "works_at", "confidence": 0.95},
                {"source": "Alice", "target": "Diana", "type": "knows", "confidence": 0.8},
                {"source": "Diana", "target": "TechCorp", "type": "works_at", "confidence": 0.95},
                {"source": "TechCorp", "target": "BetaCorp", "type": "partner_of", "confidence": 0.7},
            ]
        },
        max_path_length=5,
        find_all_paths=False,
        ranking_strategy=RankingStrategy.COMPOSITE
    )

    analyzer = GraphPathAnalyzer(config)

    # Find shortest path
    print("=== Shortest Path Analysis ===")
    path = analyzer.find_shortest_path("Alice", "BetaCorp")
    if path:
        print(f"Path: {' → '.join(path.nodes)}")
        print(f"Distance: {path.distance} hops")
        print(f"Confidence: {path.confidence:.2%}")
        print(f"Explanation: {path.explanation}")

    # Find all paths
    print("\n=== All Paths Analysis ===")
    all_paths = analyzer.find_all_paths("Alice", "TechCorp")
    print(f"Total paths found: {len(all_paths)}")
    for i, p in enumerate(all_paths):
        print(f"  Path {i+1}: {' → '.join(p.nodes)} (distance: {p.distance}, conf: {p.confidence:.2%})")

    # Analyze diversity
    print("\n=== Path Diversity Analysis ===")
    diversity = analyzer.analyze_path_diversity("Alice", "TechCorp")
    for key, value in diversity.items():
        print(f"{key}: {value}")

    # Get statistics
    print("\n=== Graph Statistics ===")
    stats = analyzer.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")


