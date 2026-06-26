"""
Path Reasoner: Analyze and reason about graph paths.

Provides path analysis, reasoning, and optimization for multi-hop queries
including path validation, cost estimation, and complexity analysis.

Author: Knowledge Graph Project
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


# ============================================================================
# Enums and Data Classes
# ============================================================================

class PathComplexity(Enum):
    """Path complexity levels."""
    LOW = "low"               # O(n) or O(n log n)
    MEDIUM = "medium"         # O(n²)
    HIGH = "high"             # O(n³)
    VERY_HIGH = "very_high"   # O(n⁴+)


@dataclass
class PathNode:
    """Node in a path."""
    label: str
    properties: Dict[str, Any] = field(default_factory=dict)

    def to_string(self) -> str:
        """Convert to string representation."""
        prop_str = ", ".join([f"{k}:{v}" for k, v in self.properties.items()])
        if prop_str:
            return f"{self.label}{{{prop_str}}}"
        return self.label


@dataclass
class PathEdge:
    """Edge in a path."""
    relationship_type: str
    direction: str = "->"  # "->", "<-", "<->"
    properties: Dict[str, Any] = field(default_factory=dict)

    def to_string(self) -> str:
        """Convert to string representation."""
        prop_str = ", ".join([f"{k}:{v}" for k, v in self.properties.items()])
        if prop_str:
            return f"-[:{self.relationship_type}{{{prop_str}}}]{self.direction}"
        return f"-[:{self.relationship_type}]{self.direction}"


@dataclass
class GraphPath:
    """Represents a graph path."""
    nodes: List[PathNode]
    edges: List[PathEdge]
    hop_count: int

    def is_valid(self) -> bool:
        """Check if path structure is valid."""
        if len(self.nodes) < 2:
            return False
        if len(self.edges) != len(self.nodes) - 1:
            return False
        return True

    def has_cycle(self) -> bool:
        """Check if path contains cycle."""
        node_labels = [n.label for n in self.nodes]
        return len(node_labels) != len(set(node_labels))

    def to_string(self) -> str:
        """Convert path to string representation."""
        path_str = self.nodes[0].to_string()
        for i, edge in enumerate(self.edges):
            path_str += edge.to_string()
            path_str += self.nodes[i + 1].to_string()
        return path_str


@dataclass
class PathAnalysis:
    """Analysis of a graph path."""
    path: GraphPath
    estimated_cost: float
    complexity: PathComplexity
    cardinality_estimate: int
    optimization_suggestions: List[str] = field(default_factory=list)
    performance_warning: Optional[str] = None


# ============================================================================
# Path Reasoner
# ============================================================================

class PathReasoner:
    """Analyzes and reasons about graph paths."""

    def __init__(self):
        """Initialize path reasoner."""
        self.complexity_thresholds = {
            1: PathComplexity.LOW,
            2: PathComplexity.MEDIUM,
            3: PathComplexity.HIGH,
            4: PathComplexity.VERY_HIGH
        }

    def analyze_path(self, path: GraphPath, cardinality: Dict[str, int] = None) -> PathAnalysis:
        """Analyze a graph path."""

        if not path.is_valid():
            raise ValueError("Invalid path structure")

        cardinality = cardinality or {}

        # Estimate complexity
        complexity = self._estimate_complexity(path.hop_count)

        # Estimate cost
        cost = self._estimate_cost(path, cardinality)

        # Estimate cardinality
        card_estimate = self._estimate_cardinality(path, cardinality)

        # Generate optimization suggestions
        suggestions = self._generate_suggestions(path, complexity, card_estimate)

        # Check for performance warnings
        warning = self._check_performance_warning(path, complexity)

        return PathAnalysis(
            path=path,
            estimated_cost=cost,
            complexity=complexity,
            cardinality_estimate=card_estimate,
            optimization_suggestions=suggestions,
            performance_warning=warning
        )

    def find_shortest_path_between(
        self,
        start_label: str,
        end_label: str,
        relationship_types: List[str]
    ) -> Optional[GraphPath]:
        """Find shortest path between node types."""

        # This would use graph algorithm in real implementation
        # For now, return template

        nodes = [PathNode(start_label), PathNode(end_label)]
        edges = [PathEdge(rel) for rel in relationship_types[:1]]

        return GraphPath(nodes=nodes, edges=edges, hop_count=1)

    def validate_path_traversal(self, path: GraphPath) -> Tuple[bool, List[str]]:
        """Validate path traversal is possible."""

        issues = []

        # Check cycle
        if path.has_cycle():
            issues.append("Path contains cycle - may cause infinite loops")

        # Check direction consistency
        directions = [e.direction for e in path.edges]
        if len(set(directions)) > 1:
            issues.append("Path has mixed directions - ensure intentional")

        # Check hop count
        if path.hop_count > 4:
            issues.append(f"High hop count ({path.hop_count}) - may be expensive")

        return len(issues) == 0, issues

    def _estimate_complexity(self, hop_count: int) -> PathComplexity:
        """Estimate path complexity."""
        bounded_hops = min(hop_count, 4)
        return self.complexity_thresholds.get(bounded_hops, PathComplexity.VERY_HIGH)

    def _estimate_cost(self, path: GraphPath, cardinality: Dict[str, int]) -> float:
        """Estimate query execution cost."""

        # Base cost: exponential in hop count
        base_cost = 10 * (5 ** (path.hop_count - 1))

        # Adjust by cardinality
        for node in path.nodes:
            if node.label in cardinality:
                base_cost *= cardinality[node.label] / 10000

        return max(1.0, base_cost)

    def _estimate_cardinality(self, path: GraphPath, cardinality: Dict[str, int]) -> int:
        """Estimate result cardinality."""

        # Start with first node cardinality
        result_card = cardinality.get(path.nodes[0].label, 1000)

        # Multiply by average branching factor per hop
        branching_factor = 3  # Average
        result_card = int(result_card * (branching_factor ** (path.hop_count - 1)))

        return result_card

    def _generate_suggestions(
        self,
        path: GraphPath,
        complexity: PathComplexity,
        cardinality: int
    ) -> List[str]:
        """Generate optimization suggestions."""

        suggestions = []

        # Complexity suggestions
        if complexity == PathComplexity.HIGH:
            suggestions.append("Consider adding WHERE conditions to filter early")
            suggestions.append("Use LIMIT to control result set size")

        elif complexity == PathComplexity.VERY_HIGH:
            suggestions.append("⚠️  Very high complexity - add strong filters")
            suggestions.append("Consider reducing hop depth or breaking into multiple queries")
            suggestions.append("Add index on starting node property")

        # Cardinality suggestions
        if cardinality > 100000:
            suggestions.append("High cardinality result set - add aggregation or LIMIT")

        # Path structure suggestions
        if path.hop_count > 3:
            suggestions.append(f"Deep traversal ({path.hop_count} hops) - consider using LIMIT")

        # Cycle detection
        if path.has_cycle():
            suggestions.append("Path contains cycle - verify this is intentional")

        return suggestions

    def _check_performance_warning(
        self,
        path: GraphPath,
        complexity: PathComplexity
    ) -> Optional[str]:
        """Check for performance issues."""

        if complexity == PathComplexity.VERY_HIGH:
            return f"⚠️  Query with {path.hop_count} hops has exponential complexity O(n^{path.hop_count})"

        if path.hop_count > 4:
            return f"⚠️  Hop count {path.hop_count} exceeds safe limit of 4"

        return None

    def explain_path(self, path: GraphPath) -> str:
        """Generate human-readable path explanation."""

        lines = []
        lines.append(f"Path with {path.hop_count} hops:")
        lines.append("")

        # Describe nodes
        for i, node in enumerate(path.nodes):
            lines.append(f"  {i+1}. {node.label}")

        lines.append("")
        lines.append("Via relationships:")

        # Describe relationships
        for i, edge in enumerate(path.edges):
            lines.append(f"  {i+1}. {edge.relationship_type} ({edge.direction})")

        return "\n".join(lines)

    def recommend_indexes(self, path: GraphPath) -> List[str]:
        """Recommend indexes for path traversal."""

        indexes = []

        # Index starting node
        if path.nodes:
            start_label = path.nodes[0].label
            indexes.append(f"CREATE INDEX ON :{start_label}(id)")

        # Index relationship types
        for edge in path.edges:
            indexes.append(f"CREATE RELATIONSHIP_INDEX ON :({edge.relationship_type})")

        # Index ending node for common filters
        if path.nodes and len(path.nodes) > 1:
            end_label = path.nodes[-1].label
            indexes.append(f"CREATE INDEX ON :{end_label}(active)")

        return indexes

    def print_analysis(self, analysis: PathAnalysis):
        """Pretty print path analysis."""

        print("\n" + "="*70)
        print("Path Analysis")
        print("="*70)

        print(f"\nPath: {analysis.path.to_string()}")
        print(f"Hops: {analysis.path.hop_count}")
        print(f"Valid: {analysis.path.is_valid()}")

        print(f"\nComplexity: {analysis.complexity.value.upper()}")
        print(f"Estimated Cost: {analysis.estimated_cost:.1f}")
        print(f"Estimated Cardinality: {analysis.cardinality_estimate:,}")

        if analysis.performance_warning:
            print(f"\n⚠️  {analysis.performance_warning}")

        if analysis.optimization_suggestions:
            print(f"\n💡 Optimization Suggestions:")
            for sugg in analysis.optimization_suggestions:
                print(f"  • {sugg}")

        print("\n" + "="*70 + "\n")


# ============================================================================
# Usage Example
# ============================================================================

if __name__ == "__main__":
    print("🚀 Path Reasoner - Example Usage\n")

    reasoner = PathReasoner()

    # Create a sample path
    path = GraphPath(
        nodes=[
            PathNode("Person"),
            PathNode("Person"),
            PathNode("Person")
        ],
        edges=[
            PathEdge("FOLLOWS"),
            PathEdge("FOLLOWS")
        ],
        hop_count=2
    )

    # Analyze path
    analysis = reasoner.analyze_path(
        path,
        cardinality={"Person": 50000}
    )

    reasoner.print_analysis(analysis)

    # Explain path
    explanation = reasoner.explain_path(path)
    print("Path Explanation:")
    print(explanation)

    # Recommend indexes
    indexes = reasoner.recommend_indexes(path)
    print("\nRecommended Indexes:")
    for idx in indexes:
        print(f"  {idx}")

    print("\n✅ Path Reasoner Ready!")

