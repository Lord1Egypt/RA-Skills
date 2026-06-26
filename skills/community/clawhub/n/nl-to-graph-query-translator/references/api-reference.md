# API Reference

## Overview

This document provides technical API reference for the Natural Language to Graph Query Translator. It details function signatures, parameters, return types, and usage examples for programmatic access to the skill.

---

## Core Functions

### `translate_nl_to_query()`

Translates natural language question to graph query.

**Signature:**
```python
def translate_nl_to_query(
    nl_question: str,
    query_language: Literal["cypher", "sparql"],
    schema: Optional[GraphSchema] = None,
    context: Optional[Dict[str, Any]] = None
) -> TranslationResult
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| nl_question | str | Yes | Natural language question to translate |
| query_language | str | Yes | Target query language: "cypher" or "sparql" |
| schema | GraphSchema | No | Graph schema for validation and hints |
| context | dict | No | Additional context (entity hints, preferences) |

**Returns:**

```python
TranslationResult(
    query: str,                    # Generated query
    query_language: str,           # "cypher" or "sparql"
    entities: List[Entity],        # Extracted entities
    relationships: List[Relationship],  # Extracted relationships
    confidence: float,             # 0.0-1.0 confidence score
    explanation: str,              # Human-readable explanation
    alternative_queries: List[str] # Alternative interpretations
)
```

**Examples:**

```python
# Basic translation
result = translate_nl_to_query(
    "Find employees at Acme",
    query_language="cypher"
)
print(result.query)
# Output: MATCH (e:Employee)-[:WORKS_AT]->(c:Company {name:"Acme"})
#         RETURN e

# With schema
schema = GraphSchema(
    nodes=[
        NodeType("Person", properties=["name", "age"]),
        NodeType("Company", properties=["name", "industry"])
    ],
    relationships=[
        RelationType("WORKS_AT", "Person", "Company")
    ]
)

result = translate_nl_to_query(
    "Show people working at Acme",
    query_language="sparql",
    schema=schema
)

# With context
context = {
    "entity_hints": {"Acme": "Company"},
    "relationship_preferences": ["direct"],
    "result_limit": 50
}

result = translate_nl_to_query(
    "Who works at Acme?",
    query_language="cypher",
    context=context
)
```

---

### `extract_entities()`

Identifies and classifies entities in text.

**Signature:**
```python
def extract_entities(
    text: str,
    schema: Optional[GraphSchema] = None,
    return_properties: bool = False
) -> List[Entity]
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| text | str | Yes | Text to extract entities from |
| schema | GraphSchema | No | Schema for entity classification |
| return_properties | bool | No | Include property values (default: False) |

**Returns:**

```python
[
    Entity(
        text: str,              # Original text span
        label: str,             # Entity type (PERSON, ORG, LOCATION, etc.)
        start: int,             # Character offset start
        end: int,               # Character offset end
        properties: Dict[str, Any]  # Extracted properties
    ),
    ...
]
```

**Example:**

```python
entities = extract_entities("Alice works at Acme earning $60,000")

for entity in entities:
    print(f"{entity.text} ({entity.label}) @ [{entity.start}:{entity.end}]")
    # Output:
    # Alice (PERSON) @ [0:5]
    # Acme (ORGANIZATION) @ [16:20]
    # $60,000 (MONEY) @ [29:36]
```

---

### `extract_relationships()`

Identifies relationships between entities.

**Signature:**
```python
def extract_relationships(
    text: str,
    entities: Optional[List[Entity]] = None,
    schema: Optional[GraphSchema] = None
) -> List[Relationship]
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| text | str | Yes | Text to extract relationships from |
| entities | List[Entity] | No | Pre-extracted entities (optional) |
| schema | GraphSchema | No | Schema for relationship validation |

**Returns:**

```python
[
    Relationship(
        entity1: Entity,        # Source entity
        entity2: Entity,        # Target entity
        relation_type: str,     # Relationship type (WORKS_AT, KNOWS, etc.)
        direction: Literal["forward", "bidirectional"],
        confidence: float,      # 0.0-1.0 confidence
        properties: Dict[str, Any]  # Relationship metadata
    ),
    ...
]
```

**Example:**

```python
rels = extract_relationships("Alice works at Acme and manages Bob")

for rel in rels:
    print(f"{rel.entity1.text} -[{rel.relation_type}]-> {rel.entity2.text}")
    # Output:
    # Alice -[WORKS_AT]-> Acme
    # Alice -[MANAGES]-> Bob
```

---

### `generate_cypher_query()`

Generates Cypher query from graph pattern.

**Signature:**
```python
def generate_cypher_query(
    pattern: GraphPattern,
    filters: Optional[List[Filter]] = None,
    return_fields: Optional[List[str]] = None,
    limit: Optional[int] = None,
    order_by: Optional[List[OrderBy]] = None
) -> str
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| pattern | GraphPattern | Yes | Node and relationship pattern |
| filters | List[Filter] | No | WHERE clause filters |
| return_fields | List[str] | No | Fields to return |
| limit | int | No | LIMIT clause |
| order_by | List[OrderBy] | No | ORDER BY clauses |

**Returns:**

```
str: Executable Cypher query
```

**Example:**

```python
pattern = GraphPattern(
    nodes=[
        Node("p", "Person", {"name": "Alice"}),
        Node("c", "Company")
    ],
    relationships=[
        Relationship("p", "WORKS_AT", "c")
    ]
)

filters = [Filter("p.age > 30")]
order_by = [OrderBy("p.name", "ASC")]

query = generate_cypher_query(
    pattern,
    filters=filters,
    return_fields=["p", "c"],
    limit=50,
    order_by=order_by
)

print(query)
# Output:
# MATCH (p:Person {name:"Alice"})-[:WORKS_AT]->(c:Company)
# WHERE p.age > 30
# RETURN p, c
# ORDER BY p.name ASC
# LIMIT 50
```

---

### `generate_sparql_query()`

Generates SPARQL query from graph pattern.

**Signature:**
```python
def generate_sparql_query(
    pattern: GraphPattern,
    prefixes: Optional[Dict[str, str]] = None,
    filters: Optional[List[Filter]] = None,
    return_variables: Optional[List[str]] = None,
    limit: Optional[int] = None,
    order_by: Optional[List[OrderBy]] = None,
    group_by: Optional[List[str]] = None
) -> str
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| pattern | GraphPattern | Yes | Node and relationship pattern |
| prefixes | Dict[str, str] | No | URI prefixes |
| filters | List[Filter] | No | FILTER clauses |
| return_variables | List[str] | No | SELECT variables |
| limit | int | No | LIMIT clause |
| order_by | List[OrderBy] | No | ORDER BY clauses |
| group_by | List[str] | No | GROUP BY clauses |

**Returns:**

```
str: Executable SPARQL query
```

**Example:**

```python
pattern = GraphPattern(
    nodes=[
        Node("?person", "Person"),
        Node("?company", "Company")
    ],
    relationships=[
        Relationship("?person", "WORKS_AT", "?company")
    ]
)

prefixes = {
    "ex": "http://example.com/",
    "foaf": "http://xmlns.com/foaf/0.1/"
}

query = generate_sparql_query(
    pattern,
    prefixes=prefixes,
    return_variables=["?person", "?company"],
    limit=50
)

print(query)
# Output:
# PREFIX ex: <http://example.com/>
# PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#
# SELECT ?person ?company
# WHERE {
#   ?person rdf:type ex:Person .
#   ?person ex:WORKS_AT ?company .
#   ?company rdf:type ex:Company .
# }
# LIMIT 50
```

---

## Data Models

### Entity

Represents an extracted entity.

```python
@dataclass
class Entity:
    text: str                       # Original text
    label: str                      # Entity type
    start: int                      # Character offset
    end: int                        # Character offset
    properties: Dict[str, Any]      # Key-value properties
    confidence: float = 1.0         # 0.0-1.0
    aliases: List[str] = None       # Alternative names
    entity_id: Optional[str] = None # Graph database ID
```

### Relationship

Represents an extracted relationship.

```python
@dataclass
class Relationship:
    entity1: Entity                 # Source
    entity2: Entity                 # Target
    relation_type: str              # Type (WORKS_AT, KNOWS, etc.)
    direction: Literal["forward", "bidirectional", "reverse"]
    properties: Dict[str, Any] = None   # Metadata
    confidence: float = 1.0         # 0.0-1.0
```

### Filter

Represents a query filter condition.

```python
@dataclass
class Filter:
    expression: str                 # Filter expression (e.g., "age > 30")
    operator: Literal["AND", "OR"]  # Logical operator
    variable: Optional[str] = None  # Variable name
```

### GraphPattern

Represents a graph query pattern.

```python
@dataclass
class GraphPattern:
    nodes: List[Node]               # Query nodes
    relationships: List[Relationship]   # Query relationships
    start_node: Optional[str] = None    # Entry point
```

### GraphSchema

Defines node and relationship types in the graph.

```python
@dataclass
class GraphSchema:
    nodes: List[NodeType]           # Node type definitions
    relationships: List[RelationType]   # Relationship type definitions
    
    @dataclass
    class NodeType:
        label: str
        properties: List[str]
        description: Optional[str] = None
    
    @dataclass
    class RelationType:
        type_name: str
        from_label: str
        to_label: str
        properties: List[str] = None
        description: Optional[str] = None
```

---

## Response Types

### TranslationResult

Complete translation response.

```python
@dataclass
class TranslationResult:
    query: str                          # Generated query
    query_language: str                 # "cypher" or "sparql"
    entities: List[Entity]              # Extracted entities
    relationships: List[Relationship]   # Extracted relationships
    confidence: float                   # Overall confidence 0.0-1.0
    explanation: str                    # Human-readable explanation
    alternative_queries: List[str]      # Alternative interpretations
    metadata: Dict[str, Any] = None     # Additional metadata
    execution_time_ms: float = 0        # Processing time
```

---

## Error Handling

### TranslationError

Raised when translation cannot be completed.

```python
class TranslationError(Exception):
    code: str                   # Error code
    message: str                # Error message
    details: Dict[str, Any]     # Additional details
    suggestions: List[str]      # Recovery suggestions
```

**Example:**

```python
try:
    result = translate_nl_to_query("unclear question", "cypher")
except TranslationError as e:
    print(f"Error {e.code}: {e.message}")
    print(f"Suggestions: {e.suggestions}")
```

### Common Error Codes

| Code | Meaning |
|------|---------|
| AMBIGUOUS_QUERY | Query could be interpreted multiple ways |
| UNKNOWN_ENTITY | Entity not recognized in schema |
| UNSUPPORTED_LANGUAGE | Query language not supported |
| SCHEMA_MISMATCH | Query doesn't match schema |
| TIMEOUT | Processing took too long |

---

## Usage Examples

### Example 1: Simple Translation

```python
from nl_translator import translate_nl_to_query

result = translate_nl_to_query(
    "Find all employees at Acme",
    query_language="cypher"
)

print("Generated Query:")
print(result.query)
print(f"\nConfidence: {result.confidence * 100}%")
print(f"Explanation: {result.explanation}")
```

### Example 2: With Schema Validation

```python
from nl_translator import translate_nl_to_query, GraphSchema, NodeType

schema = GraphSchema(
    nodes=[
        NodeType("Employee", ["name", "age", "salary"]),
        NodeType("Company", ["name", "industry", "employees"]),
        NodeType("Department", ["name", "budget"])
    ]
)

result = translate_nl_to_query(
    "Show me high-earning employees at Tech Corp",
    query_language="cypher",
    schema=schema
)

if result.confidence < 0.8:
    print("Low confidence. Alternatives:")
    for alt in result.alternative_queries:
        print(f"  - {alt}")
```

### Example 3: Batch Processing

```python
from nl_translator import translate_nl_to_query

queries = [
    "Find employees at Acme",
    "Show companies in New York",
    "Who manages Alice?"
]

for nl_query in queries:
    result = translate_nl_to_query(nl_query, "sparql")
    print(f"Q: {nl_query}")
    print(f"A: {result.query}\n")
```

---

## Rate Limiting

API rate limits apply:

- **Free tier**: 100 requests/hour
- **Pro tier**: 10,000 requests/hour
- **Enterprise**: Custom limits

---

## See Also

- [Query Patterns Reference](query-patterns.md)
- [Cypher Query Guide](cypher-query-guide.md)
- [SPARQL Query Guide](sparql-query-guide.md)

