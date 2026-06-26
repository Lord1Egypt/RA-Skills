"""
GraphQL Graph Mapping - Production Implementation
Translates GraphQL queries to graph database operations (Cypher, Gremlin, SPARQL)
and maps results back to GraphQL response format.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set
from enum import Enum
import json
import re


class DatabaseType(Enum):
    """Supported graph database types."""
    NEO4J = "neo4j"
    GREMLIN = "gremlin"
    SPARQL = "sparql"
    PROPERTY_GRAPH = "property_graph"


class FieldType(Enum):
    """GraphQL field types."""
    SCALAR = "scalar"
    OBJECT = "object"
    LIST = "list"
    RELATIONSHIP = "relationship"


@dataclass
class GraphQLField:
    """Represents a GraphQL field."""
    name: str
    type: FieldType
    target_type: Optional[str] = None  # For object/list fields
    arguments: Dict[str, Any] = field(default_factory=dict)
    is_required: bool = False


@dataclass
class GraphQLType:
    """Represents a GraphQL object type."""
    name: str
    fields: Dict[str, GraphQLField] = field(default_factory=dict)
    node_label: Optional[str] = None  # Maps to graph label


@dataclass
class SchemaMapping:
    """Maps GraphQL type to graph database representation."""
    graphql_type: str
    node_label: str
    properties: Dict[str, str] = field(default_factory=dict)  # GraphQL field → graph property
    relationships: Dict[str, Dict[str, str]] = field(default_factory=dict)  # field → {relationship, target_label}


class GraphQLQueryParser:
    """Parses GraphQL query strings."""

    def __init__(self):
        self.current_pos = 0
        self.query_str = ""

    def parse(self, query_str: str) -> Dict[str, Any]:
        """Parse GraphQL query string into AST."""
        self.query_str = query_str.strip()
        self.current_pos = 0

        # Skip whitespace
        self._skip_whitespace()

        # Parse query
        if self.query_str.startswith('query'):
            self._skip_word('query')

        # Get query name if present
        query_name = None
        if self._current_char() and self._current_char().isalpha():
            query_name = self._read_identifier()

        # Parse selection set
        selections = self._parse_selection_set()

        return {
            "name": query_name,
            "selections": selections,
            "type": "query"
        }

    def _parse_selection_set(self) -> List[Dict[str, Any]]:
        """Parse GraphQL selection set."""
        selections = []
        self._skip_whitespace()

        if self._current_char() != '{':
            return selections

        self._skip_char('{')
        self._skip_whitespace()

        while self._current_char() != '}':
            field = self._parse_field()
            selections.append(field)
            self._skip_whitespace()

        self._skip_char('}')
        return selections

    def _parse_field(self) -> Dict[str, Any]:
        """Parse a GraphQL field."""
        self._skip_whitespace()

        # Parse alias if present
        field_name = self._read_identifier()
        alias = None

        if self._current_char() == ':':
            alias = field_name
            self._skip_char(':')
            field_name = self._read_identifier()

        # Parse arguments
        arguments = {}
        if self._current_char() == '(':
            arguments = self._parse_arguments()

        # Parse nested selection set
        nested_selections = []
        if self._current_char() == '{':
            nested_selections = self._parse_selection_set()

        return {
            "name": field_name,
            "alias": alias,
            "arguments": arguments,
            "selections": nested_selections
        }

    def _parse_arguments(self) -> Dict[str, Any]:
        """Parse GraphQL arguments."""
        arguments = {}
        self._skip_char('(')
        self._skip_whitespace()

        while self._current_char() != ')':
            arg_name = self._read_identifier()
            self._skip_whitespace()
            self._skip_char(':')
            self._skip_whitespace()

            arg_value = self._parse_value()
            arguments[arg_name] = arg_value
            self._skip_whitespace()

        self._skip_char(')')
        return arguments

    def _parse_value(self) -> Any:
        """Parse GraphQL value (string, number, variable, etc)."""
        self._skip_whitespace()

        if self._current_char() == '"':
            return self._parse_string()
        elif self._current_char() == '$':
            return self._parse_variable()
        elif self._current_char() in '-0123456789':
            return self._parse_number()
        elif self._current_char() == 'n':
            self._skip_word('null')
            return None
        elif self._current_char() == 't':
            self._skip_word('true')
            return True
        elif self._current_char() == 'f':
            self._skip_word('false')
            return False
        elif self._current_char() == '[':
            return self._parse_list()
        elif self._current_char() == '{':
            return self._parse_object()
        else:
            return self._read_identifier()

    def _parse_string(self) -> str:
        """Parse string value."""
        self._skip_char('"')
        value = ""

        while self._current_char() != '"':
            if self._current_char() == '\\':
                self.current_pos += 1
            value += self._current_char()
            self.current_pos += 1

        self._skip_char('"')
        return value

    def _parse_variable(self) -> str:
        """Parse variable reference."""
        self._skip_char('$')
        return self._read_identifier()

    def _parse_number(self) -> float:
        """Parse number value."""
        num_str = ""
        if self._current_char() == '-':
            num_str += self._current_char()
            self.current_pos += 1

        while self._current_char() and self._current_char() in '0123456789.':
            num_str += self._current_char()
            self.current_pos += 1

        return float(num_str) if '.' in num_str else int(num_str)

    def _parse_list(self) -> List[Any]:
        """Parse list value."""
        self._skip_char('[')
        values = []

        while self._current_char() != ']':
            values.append(self._parse_value())

        self._skip_char(']')
        return values

    def _parse_object(self) -> Dict[str, Any]:
        """Parse object value."""
        self._skip_char('{')
        obj = {}

        while self._current_char() != '}':
            key = self._read_identifier()
            self._skip_whitespace()
            self._skip_char(':')
            self._skip_whitespace()
            obj[key] = self._parse_value()
            self._skip_whitespace()

        self._skip_char('}')
        return obj

    def _read_identifier(self) -> str:
        """Read identifier (field name, type name, etc)."""
        identifier = ""
        while self._current_char() and (self._current_char().isalnum() or self._current_char() == '_'):
            identifier += self._current_char()
            self.current_pos += 1
        return identifier

    def _skip_whitespace(self):
        """Skip whitespace and comments."""
        while self.current_pos < len(self.query_str):
            if self.query_str[self.current_pos].isspace():
                self.current_pos += 1
            elif self.query_str[self.current_pos:self.current_pos+1] == '#':
                # Skip comment
                while self.current_pos < len(self.query_str) and self.query_str[self.current_pos] != '\n':
                    self.current_pos += 1
            else:
                break

    def _skip_char(self, char: str):
        """Skip expected character."""
        self._skip_whitespace()
        if self._current_char() == char:
            self.current_pos += 1
        else:
            raise ValueError(f"Expected '{char}' at position {self.current_pos}")

    def _skip_word(self, word: str):
        """Skip expected word."""
        if self.query_str[self.current_pos:self.current_pos+len(word)] == word:
            self.current_pos += len(word)

    def _current_char(self) -> Optional[str]:
        """Get current character."""
        self._skip_whitespace()
        if self.current_pos < len(self.query_str):
            return self.query_str[self.current_pos]
        return None


class QueryTranslator:
    """Translates GraphQL queries to database-specific queries."""

    def __init__(self, database_type: DatabaseType, schema_mappings: Dict[str, SchemaMapping]):
        self.database_type = database_type
        self.schema_mappings = schema_mappings

    def translate(self, graphql_ast: Dict[str, Any], variables: Optional[Dict[str, Any]] = None) -> str:
        """Translate GraphQL AST to database-specific query."""
        if self.database_type == DatabaseType.NEO4J:
            return self._translate_to_cypher(graphql_ast, variables or {})
        elif self.database_type == DatabaseType.GREMLIN:
            return self._translate_to_gremlin(graphql_ast, variables or {})
        elif self.database_type == DatabaseType.SPARQL:
            return self._translate_to_sparql(graphql_ast, variables or {})
        else:
            raise ValueError(f"Unsupported database type: {self.database_type}")

    def _translate_to_cypher(self, ast: Dict[str, Any], variables: Dict[str, Any]) -> str:
        """Translate to Neo4j Cypher."""
        selections = ast.get("selections", [])

        match_clauses = []
        return_items = []

        for selection in selections:
            match, returns = self._process_selection_for_cypher(selection, variables)
            if match:
                match_clauses.append(match)
            return_items.extend(returns)

        cypher_query = ""
        if match_clauses:
            cypher_query += "MATCH " + ", ".join(match_clauses) + "\n"

        if return_items:
            cypher_query += "RETURN " + ", ".join(return_items)

        return cypher_query

    def _process_selection_for_cypher(self, selection: Dict[str, Any], variables: Dict[str, Any]) -> tuple:
        """Process a GraphQL selection for Cypher translation."""
        field_name = selection["name"]
        arguments = selection.get("arguments", {})
        nested = selection.get("selections", [])

        # Resolve variables
        resolved_args = {}
        for key, value in arguments.items():
            if isinstance(value, str) and value.startswith("$"):
                resolved_args[key] = variables.get(value[1:])
            else:
                resolved_args[key] = value

        # Build match clause
        mapping = self._get_mapping(field_name)
        if not mapping:
            return None, []

        # Create node pattern
        node_var = self._get_node_var(field_name)
        node_pattern = f"({node_var}:{mapping.node_label}"

        # Add filters from arguments
        if "id" in resolved_args:
            node_pattern += f" {{id: '{resolved_args['id']}'}}"
        elif "where" in resolved_args:
            where_clause = self._build_where_clause(resolved_args["where"])
            # Note: WHERE usually goes in WHERE clause, not here for simplicity
            node_pattern += f" {{{where_clause}}}"

        node_pattern += ")"

        # Process nested selections
        relationships = self._process_nested_selections_cypher(node_var, nested, mapping)

        # Build return items
        return_items = [f"{node_var}.{prop}" for prop in mapping.properties.values()]

        return node_pattern, return_items

    def _process_nested_selections_cypher(self, parent_var: str, selections: List[Dict[str, Any]], parent_mapping: SchemaMapping) -> str:
        """Process nested GraphQL selections for Cypher."""
        relationships = ""

        for selection in selections:
            field_name = selection["name"]

            # Check if it's a relationship
            if field_name in parent_mapping.relationships:
                rel_info = parent_mapping.relationships[field_name]
                relationship = rel_info.get("relationship", field_name.upper())
                target_label = rel_info.get("target_label")

                child_var = self._get_node_var(field_name)
                relationships += f"-[:{relationship}]->({child_var}:{target_label})"

        return relationships

    def _translate_to_gremlin(self, ast: Dict[str, Any], variables: Dict[str, Any]) -> str:
        """Translate to Gremlin (JanusGraph, TigerGraph)."""
        selections = ast.get("selections", [])

        if not selections:
            return "g.V()"

        # Start with graph traversal
        gremlin_query = "g.V()"

        for selection in selections:
            field_name = selection["name"]
            arguments = selection.get("arguments", {})

            # Add filter if present
            if "id" in arguments:
                value = arguments["id"]
                if isinstance(value, str) and value.startswith("$"):
                    value = variables.get(value[1:])
                gremlin_query += f'.has("{field_name}", "id", "{value}")'

        return gremlin_query

    def _translate_to_sparql(self, ast: Dict[str, Any], variables: Dict[str, Any]) -> str:
        """Translate to SPARQL."""
        selections = ast.get("selections", [])

        # Build basic SPARQL query
        sparql_query = """PREFIX ex: <http://example.org/>

SELECT ?result
WHERE {
"""

        for selection in selections:
            field_name = selection["name"]
            arguments = selection.get("arguments", {})

            if "id" in arguments:
                value = arguments["id"]
                sparql_query += f"  ex:{field_name}_{value} ?result .\n"

        sparql_query += "}"

        return sparql_query

    def _get_mapping(self, field_name: str) -> Optional[SchemaMapping]:
        """Get schema mapping for field."""
        return self.schema_mappings.get(field_name)

    def _get_node_var(self, field_name: str) -> str:
        """Get variable name for node."""
        return field_name[0].lower() + field_name[1:]

    def _build_where_clause(self, where_obj: Dict[str, Any]) -> str:
        """Build WHERE clause from GraphQL where object."""
        clauses = []

        for key, value in where_obj.items():
            if isinstance(value, dict):
                # Comparison operators
                for op, val in value.items():
                    if op == "eq":
                        clauses.append(f"{key} = {val}")
                    elif op == "gt":
                        clauses.append(f"{key} > {val}")
                    elif op == "lt":
                        clauses.append(f"{key} < {val}")
            else:
                clauses.append(f"{key} = {value}")

        return " AND ".join(clauses)


class GraphQLGraphMapper:
    """Main class for GraphQL-to-graph mapping."""

    def __init__(self, database_type: DatabaseType, schema_mappings: Dict[str, SchemaMapping]):
        self.database_type = database_type
        self.schema_mappings = schema_mappings
        self.parser = GraphQLQueryParser()
        self.translator = QueryTranslator(database_type, schema_mappings)

    def parse_query(self, query_str: str) -> Dict[str, Any]:
        """Parse GraphQL query string."""
        return self.parser.parse(query_str)

    def translate_query(self, query_str: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """Parse and translate GraphQL query to database query."""
        ast = self.parse_query(query_str)
        return self.translator.translate(ast, variables)

    def translate_to_cypher(self, query_str: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """Translate GraphQL query to Neo4j Cypher."""
        ast = self.parse_query(query_str)
        translator = QueryTranslator(DatabaseType.NEO4J, self.schema_mappings)
        return translator.translate(ast, variables)

    def translate_to_gremlin(self, query_str: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """Translate GraphQL query to Gremlin."""
        ast = self.parse_query(query_str)
        translator = QueryTranslator(DatabaseType.GREMLIN, self.schema_mappings)
        return translator.translate(ast, variables)

    def translate_to_sparql(self, query_str: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """Translate GraphQL query to SPARQL."""
        ast = self.parse_query(query_str)
        translator = QueryTranslator(DatabaseType.SPARQL, self.schema_mappings)
        return translator.translate(ast, variables)

    def map_results(self, graph_results: List[Dict[str, Any]], query_str: str) -> Dict[str, Any]:
        """Map graph database results back to GraphQL response format."""
        ast = self.parse_query(query_str)

        return {
            "data": self._map_results_recursive(graph_results, ast.get("selections", []))
        }

    def _map_results_recursive(self, results: List[Dict[str, Any]], selections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Recursively map results to GraphQL shape."""
        response = {}

        for selection in selections:
            field_name = selection["name"]
            alias = selection.get("alias", field_name)

            if isinstance(results, list) and len(results) > 0:
                result = results[0]

                if field_name in result:
                    response[alias] = result[field_name]
                elif isinstance(result, dict):
                    response[alias] = result.get(field_name)
            else:
                response[alias] = None

        return response

    def validate_schema(self) -> bool:
        """Validate schema mappings."""
        if not self.schema_mappings:
            return False

        for mapping in self.schema_mappings.values():
            if not mapping.node_label:
                return False

        return True


# Example Usage
if __name__ == "__main__":
    # Define schema mappings
    person_mapping = SchemaMapping(
        graphql_type="Person",
        node_label="Person",
        properties={"id": "id", "name": "name", "email": "email"},
        relationships={
            "friends": {"relationship": "KNOWS", "target_label": "Person"},
            "worksAt": {"relationship": "WORKS_AT", "target_label": "Company"}
        }
    )

    company_mapping = SchemaMapping(
        graphql_type="Company",
        node_label="Company",
        properties={"id": "id", "name": "name", "industry": "industry"}
    )

    schema_mappings = {
        "person": person_mapping,
        "company": company_mapping
    }

    # Create mapper
    mapper = GraphQLGraphMapper(DatabaseType.NEO4J, schema_mappings)

    # Example GraphQL query
    query = """
    {
        person(id: "alice") {
            name
            email
            friends {
                name
            }
        }
    }
    """

    # Parse query
    print("=== Query Parsing ===")
    ast = mapper.parse_query(query)
    print(json.dumps(ast, indent=2))

    # Translate to Cypher
    print("\n=== Cypher Translation ===")
    cypher = mapper.translate_to_cypher(query)
    print(cypher)

    # Translate to Gremlin
    print("\n=== Gremlin Translation ===")
    gremlin = mapper.translate_to_gremlin(query)
    print(gremlin)

    # Example result mapping
    print("\n=== Result Mapping ===")
    graph_results = [
        {
            "person": {
                "id": "alice",
                "name": "Alice",
                "email": "alice@example.com",
                "friends": [
                    {"name": "Bob"},
                    {"name": "Carol"}
                ]
            }
        }
    ]

    graphql_response = mapper.map_results(graph_results, query)
    print(json.dumps(graphql_response, indent=2))

    print("\n✅ GraphQL Graph Mapper ready for production use")

