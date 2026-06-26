# System Architecture & Design

## Overview

This document describes the architecture and design principles of the Natural Language to Graph Query Translator system.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Input (NL)                          │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
         ┌───────────────┐
         │ Preprocessing │
         │  - Tokenize   │
         │  - Normalize  │
         └───────┬───────┘
                 │
    ┌────────────┼────────────┐
    ▼            ▼            ▼
┌─────────┐ ┌─────────┐ ┌──────────┐
│ Entity  │ │Relation │ │ Intent   │
│Extraction│ │Extraction│ │Detection │
└────┬────┘ └────┬────┘ └────┬─────┘
     │           │            │
     └───────────┼────────────┘
                 ▼
         ┌──────────────────┐
         │ Query Generation │
         │ - Build Pattern  │
         │ - Validate       │
         └────────┬─────────┘
                  │
         ┌────────┴────────┐
         ▼                  ▼
    ┌────────────┐    ┌────────────┐
    │  Cypher    │    │  SPARQL    │
    │  Generator │    │  Generator │
    └────┬───────┘    └────┬───────┘
         │                 │
         └────────┬────────┘
                  ▼
         ┌──────────────────┐
         │  Validation &    │
         │  Optimization    │
         └────────┬─────────┘
                  ▼
      ┌──────────────────────┐
      │  Query Result        │
      │  - Query String      │
      │  - Explanation       │
      │  - Alternatives      │
      │  - Confidence Score  │
      └──────────────────────┘
```

---

## Core Components

### 1. Preprocessing Module

**Responsibility:** Normalize and prepare input text

**Functions:**
- Tokenization (split into words)
- POS tagging (part-of-speech)
- Lemmatization (word normalization)
- Sentence segmentation
- Case normalization

**Example:**
```
Input: "Find employees AT Acme earning > $60K"
Output: [
  Token("find", "VB", "find"),
  Token("employees", "NNS", "employee"),
  Token("at", "IN", "at"),
  Token("acme", "NNP", "acme"),
  Token("earning", "VBG", "earn"),
  Token(">", "SYM", ">"),
  Token("$60k", "CD", "60000")
]
```

---

### 2. Entity Recognition Module

**Responsibility:** Identify and classify entities

**Pipeline:**
1. Named Entity Recognition (NER)
2. Entity Classification
3. Schema Mapping
4. Property Extraction
5. Entity Linking

**Output:**
```python
[
  Entity(text="Acme", label="Company", properties={"name": "Acme"}),
  Entity(text="employees", label="Person", properties={}),
  Entity(text="$60K", label="Money", properties={"amount": 60000})
]
```

---

### 3. Relationship Extraction Module

**Responsibility:** Identify connections between entities

**Pipeline:**
1. Verb/Predicate Extraction
2. Relationship Type Mapping
3. Direction Assignment
4. Property Extraction

**Output:**
```python
[
  Relationship(
    entity1=Entity("employees"),
    entity2=Entity("Acme"),
    relation_type="WORKS_AT",
    direction="forward"
  )
]
```

---

### 4. Intent Detection Module

**Responsibility:** Classify the query intent

**Intent Types:**
- FIND/SELECT: Return entities matching criteria
- COUNT/AGGREGATE: Count or aggregate results
- EXIST/CHECK: Verify if pattern exists
- PATH: Find paths between entities
- FILTER: Apply conditional logic
- ORDER/SORT: Sort results
- LIMIT: Restrict result count

**Example:**
```
"How many employees work at Acme?"
Intent: COUNT

"Find employees earning > $50K"
Intent: FIND + FILTER
```

---

### 5. Query Pattern Builder

**Responsibility:** Construct graph patterns

**Process:**
1. Map entities to node patterns
2. Map relationships to edge patterns
3. Apply filters and conditions
4. Add aggregations if needed
5. Apply ordering and limits

**Output:**
```python
GraphPattern(
  nodes=[
    Node("e", "Employee"),
    Node("c", "Company", {"name": "Acme"})
  ],
  relationships=[
    Relationship("e", "WORKS_AT", "c")
  ],
  filters=[Filter("e.salary > 60000")],
  return_fields=["e"],
  limit=100
)
```

---

### 6. Cypher Generator

**Responsibility:** Convert patterns to Cypher

**Process:**
1. Generate MATCH clause from nodes
2. Generate relationship traversal
3. Add WHERE filters
4. Add aggregations (if needed)
5. Generate RETURN clause
6. Add ORDER BY and LIMIT

**Template:**
```
MATCH <pattern>
[WHERE <conditions>]
[WITH <aggregations>]
RETURN <fields>
[ORDER BY <sort>]
[LIMIT <count>]
```

---

### 7. SPARQL Generator

**Responsibility:** Convert patterns to SPARQL

**Process:**
1. Generate PREFIX declarations
2. Generate SELECT clause
3. Generate WHERE clause with triple patterns
4. Add FILTER clauses
5. Add GROUP BY and aggregations
6. Add ORDER BY and LIMIT

**Template:**
```
PREFIX <ns>: <uri>
SELECT <variables>
WHERE {
  <triple patterns>
  [FILTER <conditions>]
}
[GROUP BY <grouping>]
[ORDER BY <sort>]
[LIMIT <count>]
```

---

### 8. Validation & Optimization Module

**Responsibility:** Validate and optimize queries

**Validation:**
- Check against schema
- Verify relationships exist
- Validate property types
- Check for semantic errors

**Optimization:**
- Reorder clauses for efficiency
- Suggest index hints
- Recommend LIMIT for large result sets
- Identify expensive patterns

---

## Data Flow Diagram

```
Natural Language Input
        │
        ▼
┌───────────────────┐
│  Preprocessing    │
│  (Tokenize, POS)  │
└────┬──────────────┘
     │
     ├─► Entity Extraction
     │        │
     │        ▼
     │   ┌──────────────────┐
     │   │ Extracted        │
     │   │ Entities         │
     │   └────────┬─────────┘
     │            │
     ├─► Relationship Extraction
     │        │
     │        ▼
     │   ┌──────────────────┐
     │   │ Extracted        │
     │   │ Relationships    │
     │   └────────┬─────────┘
     │            │
     └─► Intent Detection
              │
              ▼
    ┌──────────────────────┐
    │ Query Pattern        │
    │ Builder              │
    │ (Combines all info)  │
    └─────────┬────────────┘
              │
         ┌────┴────┐
         ▼         ▼
    ┌─────────┐ ┌──────────┐
    │ Cypher  │ │ SPARQL   │
    │Generator│ │Generator │
    └────┬────┘ └────┬─────┘
         │           │
         └─────┬─────┘
               ▼
    ┌──────────────────────┐
    │ Validation &         │
    │ Optimization         │
    └─────────┬────────────┘
              ▼
    ┌──────────────────────┐
    │ Query Result         │
    │ (Query + Metadata)   │
    └──────────────────────┘
```

---

## Design Patterns

### 1. Pipeline Pattern

Components are organized as a pipeline where output of one becomes input of the next.

**Benefit:** 
- Easy to insert/remove steps
- Clear data flow
- Easy to debug

---

### 2. Strategy Pattern

Different generators for different query languages (Cypher, SPARQL).

**Benefit:**
- Easy to add new query languages
- Isolated language-specific logic

---

### 3. Builder Pattern

Query patterns built step-by-step.

**Benefit:**
- Flexible query construction
- Clear intermediate states

---

### 4. Factory Pattern

Create appropriate entity/relationship objects based on context.

**Benefit:**
- Centralized object creation
- Consistent validation

---

### 5. Decorator Pattern

Wrap patterns with validation/optimization.

**Benefit:**
- Non-invasive additions
- Composable functionality

---

## Integration Points

### Schema Integration

The system integrates with graph schemas to:
- Validate entities against schema labels
- Verify relationship types exist
- Check property names and types
- Infer missing information

**Schema Interface:**
```python
class GraphSchema:
    def get_node_types(self) -> List[NodeType]
    def get_relationship_types(self) -> List[RelationType]
    def validate_entity(entity: Entity) -> bool
    def validate_relationship(rel: Relationship) -> bool
    def suggest_properties(label: str) -> List[str]
```

---

### Database Integration

The system can integrate with specific database backends:

**Neo4j:**
- Cypher syntax validation
- Performance profiling
- Query execution

**RDF Stores (Virtuoso, Jena, etc.):**
- SPARQL endpoint integration
- Namespace mapping
- Query execution

---

### NLP Framework Integration

Can use different NLP libraries:

**Spacy:**
- Fast tokenization and POS tagging
- NER models
- Dependency parsing

**NLTK:**
- Lemmatization
- POS tagging
- Semantic role labeling

**Transformers (HuggingFace):**
- Advanced NER models
- Semantic understanding
- Zero-shot classification

---

## Extensibility

### Adding a New Query Language

1. Create new generator class inheriting from `BaseGenerator`
2. Implement `generate_query()` method
3. Register generator in factory
4. Add language-specific tests

---

### Adding Custom Entity Types

1. Extend entity classification rules
2. Update schema mapping
3. Add test cases for new types

---

### Adding Domain-Specific Patterns

1. Create domain pattern library
2. Integrate into pattern builder
3. Add domain-specific entity mappings

---

## Performance Considerations

### Caching

Cache expensive operations:
- Tokenization results
- NER model outputs
- Schema queries
- Query execution plans

### Lazy Evaluation

Generate queries on demand, not eagerly.

### Batch Processing

Process multiple queries efficiently.

---

## Error Handling Strategy

```
Try entity extraction
  ├─ If fails: Try to infer from context
  │
Try relationship extraction
  ├─ If fails: Suggest alternatives
  │
Try query generation
  ├─ If fails: Return error with suggestions
  │
Validate query
  ├─ If invalid: Suggest corrections
  │
Return result or error
```

---

## Security Considerations

### Input Validation

- Sanitize user input
- Check for injection attempts
- Validate parameter types

### Query Safety

- Parameterize user values
- Avoid dynamic query construction
- Escape special characters

### Authorization

- Check user permissions
- Enforce access controls
- Log query execution

---

## Testing Strategy

### Unit Testing
Test individual components in isolation.

### Integration Testing
Test component interactions.

### End-to-End Testing
Test full pipeline with sample inputs.

### Regression Testing
Maintain test suite for known issues.

---

## Deployment Architecture

```
┌─────────────────────────┐
│   API Gateway           │
└────────────┬────────────┘
             │
     ┌───────┴───────┐
     │               │
┌────▼────┐     ┌────▼────┐
│ REST    │     │ GraphQL  │
│Endpoint │     │Endpoint  │
└────┬────┘     └────┬────┘
     │               │
     └───────┬───────┘
             │
    ┌────────▼─────────┐
    │ Translator Core  │
    │ (Processing)     │
    └────────┬─────────┘
             │
     ┌───────┴───────┐
     │               │
┌────▼────┐     ┌────▼────┐
│ Neo4j   │     │ RDF     │
│ Query   │     │ Query   │
│Execution│     │Execution│
└─────────┘     └─────────┘
```

---

## Monitoring & Observability

**Metrics to track:**
- Query translation latency
- Accuracy/confidence scores
- Error rates
- Cache hit rates
- Query execution times

**Logging:**
- Translation steps
- Extracted entities/relationships
- Generated queries
- Validation results

---

## See Also

- [API Reference](references/api-reference.md)
- [Query Patterns](references/query-patterns.md)
- [Edge Cases](tests/edge-cases.md)

