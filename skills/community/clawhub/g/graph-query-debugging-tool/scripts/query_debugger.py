"""
Query Debugger: Comprehensive query analysis and debugging tool for Cypher and SPARQL.

Provides query syntax validation, schema validation, relationship analysis, 
and performance issue detection across multiple graph query languages.

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


class ErrorCategory(Enum):
    """Query error categories."""
    SYNTAX = "syntax"
    SCHEMA = "schema"
    RELATIONSHIP = "relationship"
    LOGICAL = "logical"
    PERFORMANCE = "performance"
    DATA = "data"


class Severity(Enum):
    """Error severity levels."""
    ERROR = "error"           # Query will fail
    WARNING = "warning"       # Query may fail or behave unexpectedly
    SUGGESTION = "suggestion" # Optimization opportunity


@dataclass
class SchemaElement:
    """Represents a schema element (node label, property, or relationship type)."""
    name: str
    element_type: str  # "node", "relationship", "property"
    source_label: Optional[str] = None  # For relationships
    target_label: Optional[str] = None  # For relationships
    properties: Dict[str, str] = field(default_factory=dict)  # property_name: type


@dataclass
class QueryError:
    """Represents a detected query error."""
    category: ErrorCategory
    severity: Severity
    message: str
    location: Optional[str] = None  # Line/position info
    suggestion: Optional[str] = None
    fix: Optional[str] = None


@dataclass
class AnalysisResult:
    """Complete query analysis result."""
    query: str
    query_type: QueryType
    has_errors: bool
    errors: List[QueryError] = field(default_factory=list)
    warnings: List[QueryError] = field(default_factory=list)
    suggestions: List[QueryError] = field(default_factory=list)
    nodes_found: List[str] = field(default_factory=list)
    relationships_found: List[str] = field(default_factory=list)
    properties_found: List[str] = field(default_factory=list)
    corrected_query: Optional[str] = None
    performance_issues: List[str] = field(default_factory=list)
    
    def summary(self) -> Dict:
        """Return summary statistics."""
        return {
            "query_type": self.query_type.value,
            "has_errors": self.has_errors,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "suggestion_count": len(self.suggestions),
            "nodes": len(self.nodes_found),
            "relationships": len(self.relationships_found),
            "properties": len(self.properties_found),
            "performance_issues": len(self.performance_issues)
        }


# ============================================================================
# Syntax Validators
# ============================================================================

class SyntaxValidator:
    """Validates query syntax and structure."""
    
    @staticmethod
    def validate_cypher_syntax(query: str) -> List[QueryError]:
        """Validate Cypher query syntax."""
        errors = []
        
        # Check parentheses matching
        if not SyntaxValidator._check_balanced_parens(query, "(", ")"):
            errors.append(QueryError(
                category=ErrorCategory.SYNTAX,
                severity=Severity.ERROR,
                message="Unmatched parentheses in query",
                suggestion="Ensure all '(' have matching ')'"
            ))
        
        # Check brackets matching
        if not SyntaxValidator._check_balanced_parens(query, "[", "]"):
            errors.append(QueryError(
                category=ErrorCategory.SYNTAX,
                severity=Severity.ERROR,
                message="Unmatched brackets in query",
                suggestion="Ensure all '[' have matching ']'"
            ))
        
        # Check braces matching
        if not SyntaxValidator._check_balanced_parens(query, "{", "}"):
            errors.append(QueryError(
                category=ErrorCategory.SYNTAX,
                severity=Severity.ERROR,
                message="Unmatched braces in query",
                suggestion="Ensure all '{' have matching '}'"
            ))
        
        # Check clause ordering
        clauses = ["MATCH", "OPTIONAL MATCH", "WITH", "WHERE", "RETURN", "UNION", "LIMIT"]
        clause_order = {}
        for i, clause in enumerate(clauses):
            pos = query.find(clause)
            if pos != -1:
                clause_order[clause] = pos
        
        if clause_order:
            prev_clause = None
            for clause in clauses:
                if clause in clause_order:
                    if prev_clause and clause_order[clause] < clause_order[prev_clause]:
                        errors.append(QueryError(
                            category=ErrorCategory.SYNTAX,
                            severity=Severity.WARNING,
                            message=f"Clause '{clause}' appears before '{prev_clause}'",
                            suggestion=f"Reorder: {prev_clause} should come before {clause}"
                        ))
                    prev_clause = clause
        
        return errors
    
    @staticmethod
    def validate_sparql_syntax(query: str) -> List[QueryError]:
        """Validate SPARQL query syntax."""
        errors = []
        
        # Check for matching braces
        if not SyntaxValidator._check_balanced_parens(query, "{", "}"):
            errors.append(QueryError(
                category=ErrorCategory.SYNTAX,
                severity=Severity.ERROR,
                message="Unmatched braces in SPARQL query",
                suggestion="Ensure WHERE { ... } clause is properly closed"
            ))
        
        # Check for triple statement periods
        where_match = re.search(r'WHERE\s*\{(.*?)\}', query, re.DOTALL)
        if where_match:
            where_content = where_match.group(1)
            # Count statements that should end with periods
            lines = where_content.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.endswith('.') and not line.endswith('}') and not line.endswith('{'):
                    if '?' in line and not line.startswith('OPTIONAL'):
                        errors.append(QueryError(
                            category=ErrorCategory.SYNTAX,
                            severity=Severity.WARNING,
                            message=f"SPARQL triple pattern may be missing period: {line}",
                            suggestion="Triple patterns should end with a period (.)"
                        ))
        
        # Check for SELECT clause
        if not re.search(r'(SELECT|CONSTRUCT|ASK|DESCRIBE)', query, re.IGNORECASE):
            errors.append(QueryError(
                category=ErrorCategory.SYNTAX,
                severity=Severity.ERROR,
                message="Missing SELECT/CONSTRUCT/ASK/DESCRIBE clause",
                suggestion="SPARQL queries must start with SELECT, CONSTRUCT, ASK, or DESCRIBE"
            ))
        
        return errors
    
    @staticmethod
    def _check_balanced_parens(text: str, open_char: str, close_char: str) -> bool:
        """Check if opening and closing characters are balanced."""
        count = 0
        for char in text:
            if char == open_char:
                count += 1
            elif char == close_char:
                count -= 1
            if count < 0:
                return False
        return count == 0


# ============================================================================
# Schema Validators
# ============================================================================

class SchemaValidator:
    """Validates queries against graph schema."""
    
    def __init__(self):
        """Initialize schema validator."""
        self.nodes: Dict[str, SchemaElement] = {}
        self.relationships: Dict[str, SchemaElement] = {}
        self.properties: Dict[str, SchemaElement] = {}
    
    def add_node(self, label: str, properties: Optional[Dict[str, str]] = None):
        """Add node type to schema."""
        self.nodes[label] = SchemaElement(
            name=label,
            element_type="node",
            properties=properties or {}
        )
    
    def add_relationship(self, rel_type: str, source_label: str, target_label: str):
        """Add relationship type to schema."""
        key = f"{source_label}-{rel_type}-{target_label}"
        self.relationships[key] = SchemaElement(
            name=rel_type,
            element_type="relationship",
            source_label=source_label,
            target_label=target_label
        )
    
    def validate_node_labels(self, labels: List[str]) -> List[QueryError]:
        """Validate that node labels exist in schema."""
        errors = []
        for label in labels:
            if label and label not in self.nodes:
                # Find similar labels
                similar = self._find_similar(label, list(self.nodes.keys()))
                suggestion = f"Label '{label}' not found in schema"
                if similar:
                    suggestion += f". Did you mean: {', '.join(similar)}?"
                
                errors.append(QueryError(
                    category=ErrorCategory.SCHEMA,
                    severity=Severity.ERROR if similar else Severity.WARNING,
                    message=f"Node label '{label}' not found in schema",
                    suggestion=suggestion
                ))
        return errors
    
    def validate_relationship_types(self, rel_types: List[str]) -> List[QueryError]:
        """Validate that relationship types are supported."""
        errors = []
        available_rel_types = set(elem.name for elem in self.relationships.values())
        
        for rel_type in rel_types:
            if rel_type and rel_type not in available_rel_types:
                similar = self._find_similar(rel_type, list(available_rel_types))
                suggestion = f"Relationship type '{rel_type}' not found in schema"
                if similar:
                    suggestion += f". Did you mean: {', '.join(similar)}?"
                
                errors.append(QueryError(
                    category=ErrorCategory.SCHEMA,
                    severity=Severity.WARNING,
                    message=f"Relationship type '{rel_type}' not found in schema",
                    suggestion=suggestion
                ))
        return errors
    
    def validate_properties(self, node_label: str, properties: List[str]) -> List[QueryError]:
        """Validate that properties exist for node type."""
        errors = []
        
        if node_label not in self.nodes:
            return errors  # Skip if node doesn't exist
        
        available_props = self.nodes[node_label].properties.keys()
        for prop in properties:
            if prop and prop not in available_props:
                suggestion = f"Property '{prop}' not found on {node_label} nodes"
                similar = self._find_similar(prop, list(available_props))
                if similar:
                    suggestion += f". Did you mean: {', '.join(similar)}?"
                
                errors.append(QueryError(
                    category=ErrorCategory.SCHEMA,
                    severity=Severity.WARNING,
                    message=suggestion,
                    suggestion=f"Available properties: {', '.join(sorted(available_props))}"
                ))
        return errors
    
    @staticmethod
    def _find_similar(term: str, candidates: List[str], threshold: float = 0.6) -> List[str]:
        """Find similar strings using simple Levenshtein-like matching."""
        similar = []
        term_lower = term.lower()
        
        for candidate in candidates:
            candidate_lower = candidate.lower()
            # Simple similarity: check if one contains the other or close match
            if term_lower in candidate_lower or candidate_lower in term_lower:
                similar.append(candidate)
            # Prefix match
            elif candidate_lower.startswith(term_lower[:3]):
                similar.append(candidate)
        
        return similar[:3]  # Return top 3 matches


# ============================================================================
# Query Analyzers
# ============================================================================

class QueryAnalyzer:
    """Analyzes query structure and patterns."""
    
    @staticmethod
    def extract_cypher_nodes(query: str) -> List[str]:
        """Extract node labels from Cypher query."""
        pattern = r'\([\w\s:_]*:(\w+)'
        matches = re.findall(pattern, query)
        return list(set(matches))
    
    @staticmethod
    def extract_cypher_relationships(query: str) -> List[str]:
        """Extract relationship types from Cypher query."""
        pattern = r'\[:(\w+)\]'
        matches = re.findall(pattern, query)
        return list(set(matches))
    
    @staticmethod
    def extract_cypher_properties(query: str) -> Dict[str, List[str]]:
        """Extract property references from Cypher query."""
        properties = defaultdict(list)
        # Pattern: word.property
        pattern = r'(\w+)\.(\w+)'
        matches = re.findall(pattern, query)
        for var, prop in matches:
            properties[var].append(prop)
        return dict(properties)
    
    @staticmethod
    def extract_sparql_prefixes(query: str) -> Dict[str, str]:
        """Extract SPARQL prefixes."""
        prefixes = {}
        pattern = r'PREFIX\s+(\w+):\s*<([^>]+)>'
        matches = re.findall(pattern, query, re.IGNORECASE)
        for prefix, uri in matches:
            prefixes[prefix] = uri
        return prefixes
    
    @staticmethod
    def detect_cartesian_product(query: str, query_type: QueryType) -> List[str]:
        """Detect potential Cartesian products in query."""
        issues = []
        
        if query_type == QueryType.CYPHER:
            # Look for multiple MATCH clauses without connections
            matches = re.findall(r'MATCH\s+\([^)]+\)', query, re.IGNORECASE)
            if len(matches) > 1:
                # Check if they're connected
                if 'MATCH (a:' in query and 'MATCH (b:' in query:
                    if '-[' not in query or '->' not in query:
                        issues.append(
                            "Potential Cartesian product: Multiple MATCH clauses without relationship connection"
                        )
        
        return issues
    
    @staticmethod
    def detect_inefficient_filters(query: str, query_type: QueryType) -> List[str]:
        """Detect filters that could be applied earlier."""
        issues = []
        
        if query_type == QueryType.CYPHER:
            # Check if WHERE appears late in query
            match_pos = query.find('MATCH')
            where_pos = query.find('WHERE')
            return_pos = query.find('RETURN')
            
            if where_pos > match_pos and where_pos != -1:
                # Count MATCH clauses before WHERE
                match_count = query[:where_pos].count('MATCH')
                if match_count > 1:
                    issues.append(
                        "Filter placed after multiple MATCH clauses. "
                        "Consider moving WHERE closer to relevant MATCH."
                    )
        
        return issues


# ============================================================================
# Query Debugger (Main Class)
# ============================================================================

class QueryDebugger:
    """Main query debugging tool."""
    
    def __init__(self):
        """Initialize debugger."""
        self.schema_validator = SchemaValidator()
        self.syntax_validator = SyntaxValidator()
        self.query_analyzer = QueryAnalyzer()
    
    def add_node_type(self, label: str, properties: Optional[Dict[str, str]] = None):
        """Add node type to schema for validation."""
        self.schema_validator.add_node(label, properties)
    
    def add_relationship_type(self, rel_type: str, source_label: str, target_label: str):
        """Add relationship type to schema."""
        self.schema_validator.add_relationship(rel_type, source_label, target_label)
    
    def detect_query_type(self, query: str) -> QueryType:
        """Auto-detect query type."""
        query_upper = query.upper()
        
        if 'MATCH' in query_upper or 'CREATE' in query_upper or 'MERGE' in query_upper:
            return QueryType.CYPHER
        elif 'SELECT' in query_upper or 'CONSTRUCT' in query_upper or 'ASK' in query_upper:
            return QueryType.SPARQL
        elif 'PREFIX' in query_upper and '?variable' in query:
            return QueryType.SPARQL
        
        return QueryType.UNKNOWN
    
    def analyze_query(self, query: str, query_type: Optional[QueryType] = None) -> AnalysisResult:
        """Perform comprehensive query analysis."""
        
        # Auto-detect query type if not provided
        if query_type is None:
            query_type = self.detect_query_type(query)
        
        result = AnalysisResult(
            query=query,
            query_type=query_type,
            has_errors=False
        )
        
        # 1. Syntax Validation
        if query_type == QueryType.CYPHER:
            syntax_errors = self.syntax_validator.validate_cypher_syntax(query)
        elif query_type == QueryType.SPARQL:
            syntax_errors = self.syntax_validator.validate_sparql_syntax(query)
        else:
            syntax_errors = []
        
        for error in syntax_errors:
            if error.severity == Severity.ERROR:
                result.errors.append(error)
                result.has_errors = True
            elif error.severity == Severity.WARNING:
                result.warnings.append(error)
            else:
                result.suggestions.append(error)
        
        if result.has_errors:
            return result
        
        # 2. Extract Query Elements
        if query_type == QueryType.CYPHER:
            result.nodes_found = self.query_analyzer.extract_cypher_nodes(query)
            result.relationships_found = self.query_analyzer.extract_cypher_relationships(query)
            props = self.query_analyzer.extract_cypher_properties(query)
            for var_props in props.values():
                result.properties_found.extend(var_props)
            result.properties_found = list(set(result.properties_found))
        
        # 3. Schema Validation (if schema defined)
        if self.schema_validator.nodes:
            node_errors = self.schema_validator.validate_node_labels(result.nodes_found)
            for error in node_errors:
                if error.severity == Severity.ERROR:
                    result.errors.append(error)
                    result.has_errors = True
                else:
                    result.warnings.append(error)
        
        if self.schema_validator.relationships:
            rel_errors = self.schema_validator.validate_relationship_types(result.relationships_found)
            result.warnings.extend(rel_errors)
        
        # 4. Performance Analysis
        perf_issues = self.query_analyzer.detect_cartesian_product(query, query_type)
        result.performance_issues.extend(perf_issues)
        
        perf_issues = self.query_analyzer.detect_inefficient_filters(query, query_type)
        result.performance_issues.extend(perf_issues)
        
        return result
    
    def print_analysis(self, result: AnalysisResult):
        """Pretty print analysis results."""
        print("\n" + "="*70)
        print(f"Query Debugging Analysis - {result.query_type.value.upper()}")
        print("="*70)
        
        print(f"\nQuery:\n{result.query}\n")
        
        if result.has_errors:
            print(f"❌ ERRORS ({len(result.errors)}):")
            for error in result.errors:
                print(f"  [{error.category.value}] {error.message}")
                if error.suggestion:
                    print(f"    → {error.suggestion}")
        else:
            print("✅ No critical errors found")
        
        if result.warnings:
            print(f"\n⚠️  WARNINGS ({len(result.warnings)}):")
            for warning in result.warnings:
                print(f"  [{warning.category.value}] {warning.message}")
                if warning.suggestion:
                    print(f"    → {warning.suggestion}")
        
        if result.performance_issues:
            print(f"\n📊 PERFORMANCE ISSUES ({len(result.performance_issues)}):")
            for issue in result.performance_issues:
                print(f"  • {issue}")
        
        if result.suggestions:
            print(f"\n💡 SUGGESTIONS ({len(result.suggestions)}):")
            for suggestion in result.suggestions:
                print(f"  • {suggestion.message}")
        
        print(f"\n📈 Summary: {result.summary()}")
        print("="*70 + "\n")


# ============================================================================
# Usage Examples
# ============================================================================

if __name__ == "__main__":
    # Example 1: Cypher query debugging
    print("Example 1: Cypher Query Debugging\n")
    
    debugger = QueryDebugger()
    
    # Define schema
    debugger.add_node_type("Person", {"name": "string", "age": "integer", "email": "string"})
    debugger.add_node_type("Company", {"name": "string", "industry": "string"})
    debugger.add_node_type("Department", {"name": "string"})
    
    debugger.add_relationship_type("WORKS_AT", "Person", "Company")
    debugger.add_relationship_type("IN_DEPT", "Person", "Department")
    debugger.add_relationship_type("EMPLOYS", "Company", "Person")
    
    # Test broken query 1: Missing parenthesis
    query1 = """
    MATCH (p:Person)-[:WORKS_AT]->(c:Company
    RETURN p.name, c.name
    """
    result1 = debugger.analyze_query(query1, QueryType.CYPHER)
    debugger.print_analysis(result1)
    
    # Test broken query 2: Non-existent relationship
    query2 = """
    MATCH (p:Person)-[:WORK_AT]->(c:Company)
    RETURN p.name, c.name
    """
    result2 = debugger.analyze_query(query2, QueryType.CYPHER)
    debugger.print_analysis(result2)
    
    # Test valid query
    query3 = """
    MATCH (p:Person)-[:WORKS_AT]->(c:Company)
    WHERE p.age > 30
    RETURN p.name, c.name
    """
    result3 = debugger.analyze_query(query3, QueryType.CYPHER)
    debugger.print_analysis(result3)
    
    # Example 2: SPARQL query debugging
    print("\nExample 2: SPARQL Query Debugging\n")
    
    query_sparql = """
    PREFIX ex: <http://example.org/>
    SELECT ?person
    WHERE {
      ?person rdf:type ex:Person .
      ?person ex:age ?age .
      FILTER (?age > 30)
    }
    """
    result_sparql = debugger.analyze_query(query_sparql, QueryType.SPARQL)
    debugger.print_analysis(result_sparql)
    
    print("\n✅ Query Debugging Tool Ready for Use!")

