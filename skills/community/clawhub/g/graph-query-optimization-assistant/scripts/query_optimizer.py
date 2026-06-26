"""
Query Optimizer: Comprehensive query optimization analysis for Cypher and SPARQL.

Analyzes graph queries, identifies performance bottlenecks, and recommends
optimizations including index creation, query restructuring, and cost estimation.

Author: Knowledge Graph Project
Version: 1.0.0
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple
import re
from collections import defaultdict


# ============================================================================
# Enums and Data Classes
# ============================================================================

class QueryType(Enum):
    """Supported query language types."""
    CYPHER = "cypher"
    SPARQL = "sparql"
    UNKNOWN = "unknown"


class OptimizationCategory(Enum):
    """Optimization recommendation categories."""
    NODE_SELECTION = "node_selection"
    INDEX_STRATEGY = "index_strategy"
    TRAVERSAL = "traversal"
    STRUCTURE = "structure"
    COST_ESTIMATION = "cost_estimation"
    AGGREGATION = "aggregation"
    FILTERING = "filtering"


class Severity(Enum):
    """Recommendation severity levels."""
    CRITICAL = "critical"        # Major performance issue
    HIGH = "high"                # Significant optimization opportunity
    MEDIUM = "medium"            # Moderate improvement
    LOW = "low"                  # Minor improvement


@dataclass
class IndexRecommendation:
    """Represents a recommended index."""
    node_label: str
    properties: List[str]
    index_type: str = "single"  # "single", "composite", "fulltext"
    estimated_impact: float = 0.0  # 0-1 representing improvement
    reason: str = ""


@dataclass
class OptimizationSuggestion:
    """Represents an optimization suggestion."""
    category: OptimizationCategory
    severity: Severity
    title: str
    description: str
    optimized_query: Optional[str] = None
    performance_impact: float = 0.0  # Estimated speedup multiplier (e.g., 2.5x)
    estimated_savings: str = ""


@dataclass
class PerformanceMetrics:
    """Performance metrics for a query."""
    estimated_cost: float = 0.0
    estimated_execution_time_ms: float = 0.0
    estimated_nodes_visited: int = 0
    estimated_memory_mb: float = 0.0
    cardinality_estimate: int = 0


@dataclass
class AnalysisResult:
    """Complete query optimization analysis result."""
    query: str
    query_type: QueryType
    suggestions: List[OptimizationSuggestion] = field(default_factory=list)
    index_recommendations: List[IndexRecommendation] = field(default_factory=list)
    metrics_original: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    metrics_optimized: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    optimized_query: Optional[str] = None

    def summary(self) -> Dict:
        """Return summary statistics."""
        cost_improvement = (
            (self.metrics_original.estimated_cost - self.metrics_optimized.estimated_cost) /
            self.metrics_original.estimated_cost * 100
            if self.metrics_original.estimated_cost > 0 else 0
        )

        return {
            "query_type": self.query_type.value,
            "suggestion_count": len(self.suggestions),
            "index_count": len(self.index_recommendations),
            "cost_improvement_percent": cost_improvement,
            "estimated_speedup": round(
                self.metrics_original.estimated_cost /
                max(self.metrics_optimized.estimated_cost, 0.1), 2
            )
        }


# ============================================================================
# Cost Analyzer
# ============================================================================

class QueryCostAnalyzer:
    """Analyzes and estimates query costs."""

    def __init__(self):
        self.node_cardinality = defaultdict(lambda: 1000000)  # Default cardinality
        self.relationship_cardinality = defaultdict(lambda: 5)  # Avg relationships per node

    def set_node_cardinality(self, label: str, cardinality: int):
        """Set estimated cardinality for a node type."""
        self.node_cardinality[label] = cardinality

    def estimate_cypher_cost(self, query: str) -> PerformanceMetrics:
        """Estimate cost of Cypher query."""
        metrics = PerformanceMetrics()

        # Extract MATCH patterns
        match_patterns = re.findall(r'MATCH\s+\(([^)]+)\)', query, re.IGNORECASE)

        total_cost = 0.0
        nodes_visited = 0

        for pattern in match_patterns:
            # Parse pattern for label and properties
            label_match = re.search(r':(\w+)', pattern)
            if label_match:
                label = label_match.group(1)
                cost = self.node_cardinality[label]

                # Reduce cost if pattern includes property filter
                if '{' in pattern and '}' in pattern:
                    cost *= 0.01  # 99% reduction with indexed property

                total_cost += cost
                nodes_visited += int(cost)

        # Adjust for relationships
        rel_matches = re.findall(r'\[:(\w+)\]', query)
        rel_cost = len(rel_matches) * 5  # Average 5 relationships traversed
        total_cost += rel_cost
        nodes_visited += int(rel_cost)

        # WHERE clause reduces cardinality
        if 'WHERE' in query.upper():
            where_conditions = len(re.findall(r'(?:AND|OR)', query, re.IGNORECASE)) + 1
            selectivity = 0.5 ** where_conditions
            total_cost *= selectivity
            nodes_visited = int(nodes_visited * selectivity)

        # Aggregation impact
        if 'COLLECT' in query.upper() or 'GROUP BY' in query.upper():
            total_cost *= 1.2  # 20% overhead for aggregation

        # Convert to metrics
        metrics.estimated_cost = total_cost
        metrics.estimated_nodes_visited = max(1, nodes_visited)
        metrics.estimated_execution_time_ms = total_cost * 0.001  # 1ms per unit cost
        metrics.estimated_memory_mb = nodes_visited / 10000  # Rough estimate

        return metrics

    def estimate_sparql_cost(self, query: str) -> PerformanceMetrics:
        """Estimate cost of SPARQL query."""
        metrics = PerformanceMetrics()

        # Count triple patterns
        triple_patterns = len(re.findall(r'(\?|\w+)\s+(\w+:)?\w+\s+(\?|\w+)', query))

        # Start with large cardinality for triples
        cost = 1000000.0 * (triple_patterns ** 1.5)

        # FILTER reduces cost
        filter_count = len(re.findall(r'FILTER\s*\(', query, re.IGNORECASE))
        if filter_count > 0:
            cost *= (0.5 ** filter_count)  # Each filter halves cardinality

        # LIMIT reduces final processing
        limit_match = re.search(r'LIMIT\s+(\d+)', query, re.IGNORECASE)
        if limit_match:
            limit_value = int(limit_match.group(1))
            cost = min(cost, limit_value * 100)  # Lower bound

        metrics.estimated_cost = cost
        metrics.estimated_nodes_visited = int(cost)
        metrics.estimated_execution_time_ms = cost * 0.0001
        metrics.estimated_memory_mb = cost / 50000

        return metrics


# ============================================================================
# Index Analyzer
# ============================================================================

class IndexAnalyzer:
    """Recommends indexes for query optimization."""

    @staticmethod
    def analyze_cypher_indexes(query: str) -> List[IndexRecommendation]:
        """Recommend indexes for Cypher query."""
        recommendations = []

        # Find WHERE conditions
        where_clause = re.search(r'WHERE\s+(.+?)(?:RETURN|$)', query, re.IGNORECASE | re.DOTALL)
        if where_clause:
            conditions = where_clause.group(1)

            # Find property filters
            property_filters = re.findall(r'(\w+)\.(\w+)\s*[=<>]', conditions)
            for var, prop in property_filters:
                # Find the label for this variable
                label_match = re.search(rf'\((\w+):(\w+)', query)
                if label_match:
                    var_name = label_match.group(1)
                    label = label_match.group(2)

                    if var_name == var:
                        recommendations.append(IndexRecommendation(
                            node_label=label,
                            properties=[prop],
                            index_type="single",
                            estimated_impact=0.9,
                            reason=f"Property '{prop}' frequently used in WHERE clause"
                        ))

        # Find properties used in property filters
        property_matches = re.findall(r':(\w+)\s*\{([^}]+)\}', query)
        for label, props in property_matches:
            prop_list = re.findall(r'(\w+):', props)
            if prop_list:
                recommendations.append(IndexRecommendation(
                    node_label=label,
                    properties=prop_list,
                    index_type="composite" if len(prop_list) > 1 else "single",
                    estimated_impact=0.95,
                    reason=f"Properties used in node pattern filter for {label}"
                ))

        return recommendations

    @staticmethod
    def analyze_sparql_indexes(query: str) -> List[IndexRecommendation]:
        """Recommend indexes for SPARQL query."""
        recommendations = []

        # Find FILTER conditions with property patterns
        filter_patterns = re.findall(r'FILTER\s*\(([^)]+)\)', query, re.IGNORECASE)
        for filter_expr in filter_patterns:
            # Look for property references
            props = re.findall(r'ex:(\w+)', filter_expr)
            if props:
                recommendations.append(IndexRecommendation(
                    node_label="Resource",
                    properties=props,
                    index_type="single",
                    estimated_impact=0.85,
                    reason=f"Properties used in FILTER conditions"
                ))

        return recommendations


# ============================================================================
# Query Optimizer (Main Class)
# ============================================================================

class QueryOptimizer:
    """Main query optimization engine."""

    def __init__(self):
        """Initialize optimizer."""
        self.cost_analyzer = QueryCostAnalyzer()
        self.index_analyzer = IndexAnalyzer()
        self.schema_nodes = {}
        self.schema_relationships = {}

    def add_node_type(self, label: str, cardinality: int = 1000000,
                     properties: Optional[Dict[str, str]] = None):
        """Add node type to schema."""
        self.schema_nodes[label] = {
            "cardinality": cardinality,
            "properties": properties or {}
        }
        self.cost_analyzer.set_node_cardinality(label, cardinality)

    def add_relationship_type(self, rel_type: str, source_label: str,
                             target_label: str, avg_cardinality: int = 5):
        """Add relationship type to schema."""
        key = f"{source_label}-{rel_type}-{target_label}"
        self.schema_relationships[key] = {
            "avg_cardinality": avg_cardinality
        }

    def detect_query_type(self, query: str) -> QueryType:
        """Auto-detect query type."""
        query_upper = query.upper()

        if 'MATCH' in query_upper or 'CREATE' in query_upper or 'MERGE' in query_upper:
            return QueryType.CYPHER
        elif 'SELECT' in query_upper or 'CONSTRUCT' in query_upper:
            return QueryType.SPARQL

        return QueryType.UNKNOWN

    def analyze_query(self, query: str, query_type: Optional[QueryType] = None) -> AnalysisResult:
        """Perform comprehensive query optimization analysis."""

        if query_type is None:
            query_type = self.detect_query_type(query)

        result = AnalysisResult(query=query, query_type=query_type)

        # Estimate original query cost
        if query_type == QueryType.CYPHER:
            result.metrics_original = self.cost_analyzer.estimate_cypher_cost(query)
            result.index_recommendations = self.index_analyzer.analyze_cypher_indexes(query)
        elif query_type == QueryType.SPARQL:
            result.metrics_original = self.cost_analyzer.estimate_sparql_cost(query)
            result.index_recommendations = self.index_analyzer.analyze_sparql_indexes(query)

        # Generate optimization suggestions
        result.suggestions = self._generate_suggestions(query, query_type)

        # Simulate optimized query metrics
        optimization_factor = 1 + (len(result.suggestions) * 0.1)
        result.metrics_optimized = PerformanceMetrics(
            estimated_cost=result.metrics_original.estimated_cost / optimization_factor,
            estimated_execution_time_ms=result.metrics_original.estimated_execution_time_ms / optimization_factor,
            estimated_nodes_visited=max(1, result.metrics_original.estimated_nodes_visited // int(optimization_factor)),
            estimated_memory_mb=result.metrics_original.estimated_memory_mb / optimization_factor,
            cardinality_estimate=result.metrics_original.cardinality_estimate
        )

        return result

    def _generate_suggestions(self, query: str, query_type: QueryType) -> List[OptimizationSuggestion]:
        """Generate optimization suggestions for query."""
        suggestions = []

        if query_type == QueryType.CYPHER:
            suggestions.extend(self._analyze_cypher(query))
        elif query_type == QueryType.SPARQL:
            suggestions.extend(self._analyze_sparql(query))

        return sorted(suggestions, key=lambda x: x.severity.value, reverse=True)

    def _analyze_cypher(self, query: str) -> List[OptimizationSuggestion]:
        """Analyze Cypher query for optimizations."""
        suggestions = []

        # Check for unbounded traversal
        if re.search(r'-\[\*\]-', query):
            suggestions.append(OptimizationSuggestion(
                category=OptimizationCategory.TRAVERSAL,
                severity=Severity.CRITICAL,
                title="Unbounded Traversal",
                description="Query uses unbounded traversal pattern -[*]- which can traverse entire graph",
                optimized_query="Use bounded pattern like -[*1..3]- instead",
                performance_impact=100.0
            ))

        # Check for missing WHERE filters
        if 'MATCH' in query and 'WHERE' not in query:
            suggestions.append(OptimizationSuggestion(
                category=OptimizationCategory.FILTERING,
                severity=Severity.HIGH,
                title="Missing WHERE Filter",
                description="Query lacks WHERE clause for early filtering",
                performance_impact=3.0
            ))

        # Check for late LIMIT
        if 'RETURN' in query and 'LIMIT' not in query.upper():
            suggestions.append(OptimizationSuggestion(
                category=OptimizationCategory.STRUCTURE,
                severity=Severity.MEDIUM,
                title="Missing LIMIT",
                description="Consider adding LIMIT to control result set size",
                performance_impact=2.0
            ))

        # Check for unspecified relationship types
        if re.search(r'-\[[^:\]]*\]-', query):
            suggestions.append(OptimizationSuggestion(
                category=OptimizationCategory.TRAVERSAL,
                severity=Severity.HIGH,
                title="Unspecified Relationship Type",
                description="Relationship patterns should specify type for efficiency",
                performance_impact=5.0
            ))

        return suggestions

    def _analyze_sparql(self, query: str) -> List[OptimizationSuggestion]:
        """Analyze SPARQL query for optimizations."""
        suggestions = []

        # Check triple pattern count
        triple_count = len(re.findall(r'[?]\w+\s+\w+:?\w+\s+[?]\w+', query))
        if triple_count > 5:
            suggestions.append(OptimizationSuggestion(
                category=OptimizationCategory.STRUCTURE,
                severity=Severity.MEDIUM,
                title="Many Triple Patterns",
                description=f"Query has {triple_count} triple patterns - consider simplification",
                performance_impact=2.0
            ))

        # Check for OPTIONAL without early filtering
        if 'OPTIONAL' in query and 'FILTER' not in query:
            suggestions.append(OptimizationSuggestion(
                category=OptimizationCategory.FILTERING,
                severity=Severity.MEDIUM,
                title="OPTIONAL Without Filters",
                description="OPTIONAL patterns without FILTER may match large result sets",
                performance_impact=3.0
            ))

        # Check for missing LIMIT
        if 'LIMIT' not in query.upper():
            suggestions.append(OptimizationSuggestion(
                category=OptimizationCategory.STRUCTURE,
                severity=Severity.LOW,
                title="Consider Adding LIMIT",
                description="Add LIMIT clause to control result set size",
                performance_impact=1.5
            ))

        return suggestions

    def print_analysis(self, result: AnalysisResult):
        """Pretty print analysis results."""
        print("\n" + "="*70)
        print(f"Query Optimization Analysis - {result.query_type.value.upper()}")
        print("="*70)

        print(f"\n📊 Original Query Metrics:")
        print(f"  Cost Score: {result.metrics_original.estimated_cost:.1f}")
        print(f"  Est. Time: {result.metrics_original.estimated_execution_time_ms:.1f} ms")
        print(f"  Nodes Visited: {result.metrics_original.estimated_nodes_visited:,}")
        print(f"  Memory: {result.metrics_original.estimated_memory_mb:.1f} MB")

        if result.suggestions:
            print(f"\n💡 Optimization Suggestions ({len(result.suggestions)}):")
            for i, suggestion in enumerate(result.suggestions, 1):
                print(f"  {i}. {suggestion.title} [{suggestion.severity.value}]")
                print(f"     {suggestion.description}")
                print(f"     Estimated Impact: {suggestion.performance_impact:.1f}x faster")

        if result.index_recommendations:
            print(f"\n📚 Index Recommendations ({len(result.index_recommendations)}):")
            for i, index in enumerate(result.index_recommendations, 1):
                props = ", ".join(index.properties)
                print(f"  {i}. CREATE INDEX ON :{index.node_label}({props})")
                print(f"     Impact: {index.estimated_impact*100:.0f}% - {index.reason}")

        print(f"\n⚡ Optimized Query Metrics:")
        print(f"  Cost Score: {result.metrics_optimized.estimated_cost:.1f}")
        print(f"  Est. Time: {result.metrics_optimized.estimated_execution_time_ms:.1f} ms")
        print(f"  Nodes Visited: {result.metrics_optimized.estimated_nodes_visited:,}")
        print(f"  Memory: {result.metrics_optimized.estimated_memory_mb:.1f} MB")

        summary = result.summary()
        print(f"\n📈 Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")

        print("="*70 + "\n")


# ============================================================================
# Usage Examples
# ============================================================================

if __name__ == "__main__":
    print("🚀 Query Optimizer - Example Usage\n")

    optimizer = QueryOptimizer()

    # Define schema
    optimizer.add_node_type("Person", cardinality=100000,
                           properties={"name": "string", "age": "integer"})
    optimizer.add_node_type("Company", cardinality=10000,
                           properties={"name": "string", "industry": "string"})

    optimizer.add_relationship_type("WORKS_AT", "Person", "Company", avg_cardinality=5)

    # Example 1: Inefficient query
    query1 = """
    MATCH (p:Person)-[:WORKS_AT]->(c:Company)
    WHERE c.name = "Acme"
    RETURN p
    """

    result1 = optimizer.analyze_query(query1, QueryType.CYPHER)
    optimizer.print_analysis(result1)

    # Example 2: Query with unbounded traversal
    query2 = """
    MATCH (p:Person)-[*]->(target)
    RETURN p, target
    """

    result2 = optimizer.analyze_query(query2, QueryType.CYPHER)
    optimizer.print_analysis(result2)

    print("\n✅ Query Optimizer Ready for Use!")

