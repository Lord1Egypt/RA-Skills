"""
Query Validator and Optimizer: Validate and optimize translated queries.

Provides query validation, syntax checking, optimization recommendations,
and execution planning for translated natural language queries.

Author: Knowledge Graph Project
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


# ============================================================================
# Enums and Data Classes
# ============================================================================

class ValidationStatus(Enum):
    """Query validation status."""
    VALID = "valid"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class ValidationIssue:
    """Validation issue."""
    status: ValidationStatus
    message: str
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class QueryValidation:
    """Complete query validation result."""
    query: str
    language: str
    is_valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    optimization_suggestions: List[str] = field(default_factory=list)
    estimated_execution_time_ms: float = 0.0


# ============================================================================
# Query Validator
# ============================================================================

class QueryValidator:
    """Validates translated graph queries."""

    def __init__(self, language: str = "cypher"):
        """Initialize validator."""
        self.language = language.lower()
        self.valid_cypher_keywords = {
            'MATCH', 'WHERE', 'RETURN', 'LIMIT', 'ORDER BY',
            'WITH', 'OPTIONAL', 'DISTINCT', 'COUNT', 'GROUP BY'
        }
        self.valid_sparql_keywords = {
            'SELECT', 'WHERE', 'LIMIT', 'ORDER BY', 'PREFIX',
            'OPTIONAL', 'FILTER', 'GROUP BY', 'DISTINCT'
        }

    def validate(self, query: str) -> QueryValidation:
        """Validate a graph query."""

        issues = []

        if self.language == "cypher":
            issues = self._validate_cypher(query)
        elif self.language == "sparql":
            issues = self._validate_sparql(query)

        # Generate optimization suggestions
        suggestions = self._generate_optimization_suggestions(query, issues)

        # Estimate execution time
        est_time = self._estimate_execution_time(query)

        is_valid = not any(i.status == ValidationStatus.ERROR for i in issues)

        return QueryValidation(
            query=query,
            language=self.language,
            is_valid=is_valid,
            issues=issues,
            optimization_suggestions=suggestions,
            estimated_execution_time_ms=est_time
        )

    def _validate_cypher(self, query: str) -> List[ValidationIssue]:
        """Validate Cypher query."""
        issues = []

        lines = query.split('\n')

        # Check for MATCH clause
        if not any('MATCH' in line.upper() for line in lines):
            issues.append(ValidationIssue(
                status=ValidationStatus.ERROR,
                message="Missing MATCH clause",
                suggestion="Cypher queries must start with MATCH, WITH, or UNWIND"
            ))

        # Check for RETURN clause
        if not any('RETURN' in line.upper() for line in lines):
            issues.append(ValidationIssue(
                status=ValidationStatus.ERROR,
                message="Missing RETURN clause",
                suggestion="Cypher queries must have a RETURN clause"
            ))

        # Check for LIMIT (optional but recommended)
        if not any('LIMIT' in line.upper() for line in lines):
            if not any('COUNT' in line.upper() for line in lines):
                issues.append(ValidationIssue(
                    status=ValidationStatus.WARNING,
                    message="No LIMIT clause",
                    suggestion="Add LIMIT to prevent large result sets"
                ))

        # Check for unbounded traversal
        if '-[*]-' in query:
            issues.append(ValidationIssue(
                status=ValidationStatus.WARNING,
                message="Unbounded relationship traversal",
                suggestion="Use -[*1..3]- to limit traversal depth"
            ))

        # Check for Cartesian products
        if query.count('MATCH') > 1 and 'WHERE' not in query.upper():
            issues.append(ValidationIssue(
                status=ValidationStatus.WARNING,
                message="Multiple MATCH clauses without WHERE",
                suggestion="Add WHERE conditions to prevent Cartesian products"
            ))

        return issues

    def _validate_sparql(self, query: str) -> List[ValidationIssue]:
        """Validate SPARQL query."""
        issues = []

        lines = query.split('\n')

        # Check for SELECT clause
        if not any('SELECT' in line.upper() for line in lines):
            issues.append(ValidationIssue(
                status=ValidationStatus.ERROR,
                message="Missing SELECT clause",
                suggestion="SPARQL queries must start with SELECT, CONSTRUCT, or ASK"
            ))

        # Check for WHERE clause
        if not any('WHERE' in line.upper() for line in lines):
            issues.append(ValidationIssue(
                status=ValidationStatus.ERROR,
                message="Missing WHERE clause",
                suggestion="SPARQL queries must have a WHERE clause"
            ))

        # Check for PREFIX declarations
        prefixes_used = []
        for line in lines:
            if ':' in line and 'PREFIX' not in line.upper():
                prefix = line.split(':')[0].strip()
                if prefix and not prefix.startswith('?'):
                    prefixes_used.append(prefix)

        prefixes_declared = [line for line in lines if 'PREFIX' in line.upper()]

        if prefixes_used and not prefixes_declared:
            issues.append(ValidationIssue(
                status=ValidationStatus.WARNING,
                message="Prefix used without declaration",
                suggestion="Declare prefixes with PREFIX declarations"
            ))

        # Check for LIMIT
        if not any('LIMIT' in line.upper() for line in lines):
            issues.append(ValidationIssue(
                status=ValidationStatus.WARNING,
                message="No LIMIT clause",
                suggestion="Add LIMIT to control result set size"
            ))

        return issues

    def _generate_optimization_suggestions(
        self,
        query: str,
        issues: List[ValidationIssue]
    ) -> List[str]:
        """Generate optimization suggestions."""

        suggestions = []

        # Check for missing indexes
        if 'WHERE' in query.upper():
            suggestions.append("Ensure indexes exist on frequently filtered properties")

        # Check query complexity
        if query.count('MATCH') > 2:
            suggestions.append("Query has multiple MATCH clauses - consider breaking into steps")

        # Check for inefficient patterns
        if '-[*]' in query and '1..' not in query:
            suggestions.append("Unbounded traversal - use bounded patterns")

        # Check for aggregation
        if any(word in query.upper() for word in ['COUNT', 'SUM', 'AVG', 'MAX', 'MIN']):
            suggestions.append("Consider using GROUP BY to organize aggregated results")

        # Check for large result sets
        if 'LIMIT' not in query.upper():
            suggestions.append("Add LIMIT clause to prevent large result sets")

        return suggestions

    def _estimate_execution_time(self, query: str) -> float:
        """Estimate query execution time."""

        # Simple estimation based on query complexity
        base_time = 10.0  # ms

        # Add time for MATCH clauses
        match_count = query.upper().count('MATCH')
        base_time += match_count * 20

        # Add time for relationships
        if '-[' in query:
            base_time += 50

        # Reduce time if has LIMIT
        if 'LIMIT' in query.upper():
            base_time *= 0.5

        # Add time for aggregations
        if any(word in query.upper() for word in ['COUNT', 'SUM', 'AVG']):
            base_time += 30

        return base_time

    def print_validation(self, validation: QueryValidation):
        """Pretty print validation results."""

        print("\n" + "="*70)
        print(f"Query Validation - {validation.language.upper()}")
        print("="*70)

        status_symbol = "✅" if validation.is_valid else "❌"
        print(f"\n{status_symbol} Status: {'VALID' if validation.is_valid else 'INVALID'}")

        if validation.issues:
            print(f"\nIssues ({len(validation.issues)}):")
            for issue in validation.issues:
                symbol = "❌" if issue.status == ValidationStatus.ERROR else "⚠️"
                print(f"\n{symbol} {issue.status.value.upper()}: {issue.message}")
                if issue.suggestion:
                    print(f"   Suggestion: {issue.suggestion}")

        if validation.optimization_suggestions:
            print(f"\n💡 Optimization Suggestions ({len(validation.optimization_suggestions)}):")
            for sugg in validation.optimization_suggestions:
                print(f"  • {sugg}")

        print(f"\n⏱️  Estimated Execution Time: {validation.estimated_execution_time_ms:.1f} ms")

        print("\n" + "="*70 + "\n")


# ============================================================================
# Query Optimizer
# ============================================================================

class QueryOptimizer:
    """Optimizes translated queries for better performance."""

    @staticmethod
    def optimize_cypher(query: str) -> str:
        """Optimize Cypher query."""

        optimized = query

        # Add LIMIT if missing (for safety)
        if 'LIMIT' not in optimized.upper():
            optimized += "\nLIMIT 100"

        # Replace unbounded traversal
        optimized = optimized.replace('-[*]-', '-[*1..3]-')
        optimized = optimized.replace('-[*]', '-[*1..3]')

        # Move WHERE clauses earlier
        if 'WHERE' in optimized.upper():
            # This is a simple heuristic
            pass

        return optimized

    @staticmethod
    def optimize_sparql(query: str) -> str:
        """Optimize SPARQL query."""

        optimized = query

        # Add LIMIT if missing
        if 'LIMIT' not in optimized.upper():
            optimized += "\nLIMIT 100"

        return optimized

    @staticmethod
    def print_optimization(original: str, optimized: str):
        """Print optimization comparison."""

        print("\n" + "="*70)
        print("Query Optimization")
        print("="*70)

        print("\nOriginal:")
        print(original)

        print("\nOptimized:")
        print(optimized)

        print("\n" + "="*70 + "\n")


# ============================================================================
# Usage Example
# ============================================================================

if __name__ == "__main__":
    print("🚀 Query Validator and Optimizer - Example Usage\n")

    # Example queries
    cypher_query = """MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE c.name = "Acme"
RETURN p"""

    sparql_query = """PREFIX ex: <http://example.org/>
SELECT ?person
WHERE {
  ?person ex:worksAt ex:Acme .
}"""

    # Validate Cypher
    validator = QueryValidator("cypher")
    cypher_validation = validator.validate(cypher_query)
    validator.print_validation(cypher_validation)

    # Validate SPARQL
    validator_sparql = QueryValidator("sparql")
    sparql_validation = validator_sparql.validate(sparql_query)
    validator_sparql.print_validation(sparql_validation)

    # Optimize
    optimizer = QueryOptimizer()
    unoptimized = "MATCH (p:Person)-[*]-(c:Company) RETURN p"
    optimized = optimizer.optimize_cypher(unoptimized)
    optimizer.print_optimization(unoptimized, optimized)

    print("✅ Query Validator and Optimizer Ready!")

