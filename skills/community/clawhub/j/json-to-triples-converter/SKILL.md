---
name: json_triples_converter
title: JSON to Triples Converter
description: Convert JSON documents into RDF triples or graph-ready subject–predicate–object statements for knowledge graphs and semantic databases.
category: data-ingestion
tags:
  - json-processing
  - rdf-triples
  - semantic-web
  - linked-data
  - knowledge-graph
  - json-ld
  - data-transformation
  - ontology-mapping
  - uri-generation
  - developer-tools
version: 1.0.0
author: community
license: MIT
metadata:
  {"openclaw":{"emoji":"🔗","homepage":"https://clawhub.com"}}
---

# JSON to Triples Converter

**Transform JSON documents into RDF triples and graph-ready structures.**

This skill converts hierarchical JSON data into **subject–predicate–object triples**, enabling the data to be ingested into **knowledge graphs, semantic web systems, and graph databases**. The generated triples can be exported in multiple formats including RDF Turtle, N-Triples, JSON-LD, and Graph JSON.

## Quick Start

### Use When
- Converting JSON datasets to RDF triples
- Transforming JSON APIs into knowledge graphs
- Creating semantic web representations from JSON
- Building linked data from structured JSON
- Converting JSON to JSON-LD for semantic markup
- Preparing JSON for graph database ingestion
- Extracting semantic relationships from JSON

### Inputs
- JSON documents or data structures
- Entity type specifications
- Property-to-predicate mappings
- Namespace/URI definitions
- Output format preferences
- Custom mapping rules
- Vocabulary specifications (schema.org, FOAF, etc.)

### Outputs
- RDF Turtle triples
- N-Triples format
- JSON-LD documents
- Graph JSON (nodes/edges)
- Property graph structures
- Semantic metadata
- URI mappings

## Example

**Input JSON:**
```json
{
  "person": {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com",
    "company": {
      "name": "Acme Corp",
      "industry": "Technology"
    }
  }
}
```

**Generated RDF Triples (Turtle):**
```turtle
@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix schema: <http://schema.org/> .

ex:person_alice a foaf:Person ;
  foaf:name "Alice" ;
  foaf:age 30 ;
  foaf:mbox "alice@example.com" ;
  schema:worksFor ex:company_acme .

ex:company_acme a schema:Organization ;
  foaf:name "Acme Corp" ;
  schema:industry "Technology" .
```

## JSON-to-Triples Conversion Strategy

### 1. JSON Structure Analysis
Analyze the JSON document to understand:
- Root entities (objects)
- Entity properties (keys)
- Nested relationships (nested objects)
- Arrays and collections
- Data types and literals

### 2. Entity Identification
Detect entities that represent real-world objects:
- **Person** - Individual entities
- **Organization** - Companies, groups
- **Product** - Items, goods
- **Location** - Places, regions
- **Event** - Occurrences, activities
- **Custom** - Domain-specific entities

### 3. Subject Generation
Create unique URIs for each entity:
```
Person "Alice" → ex:person_alice
Company "Acme" → ex:company_acme
Location "New York" → ex:location_newyork
```

### 4. Predicate Mapping
Map JSON keys to RDF predicates:
```
"name" → foaf:name
"age" → foaf:age
"worksFor" → schema:worksFor
"email" → foaf:mbox
```

### 5. Object Generation
Generate appropriate object values:
```
Literal values: "Alice", 30, true
References: ex:company_acme (URI reference)
Typed literals: "2024-04-09"^^xsd:date
```

### 6. Relationship Extraction
Convert nested objects to relationships:
```json
{
  "employee": {
    "name": "Alice",
    "manager": {
      "name": "Bob"
    }
  }
}
```

Becomes:
```turtle
ex:employee_alice schema:manager ex:person_bob .
```

### 7. Deduplication
Ensure shared entities are represented once:
- Same entity referenced multiple times → Single URI
- Identical values → Deduplicated
- Entity linking across documents

## Conversion Patterns

### Simple Property Mapping
```json
{"name": "Alice", "age": 30}
↓
ex:subject foaf:name "Alice" .
ex:subject foaf:age 30 .
```

### Nested Object Pattern
```json
{"person": {"name": "Alice", "company": {"name": "Acme"}}}
↓
ex:person_alice foaf:name "Alice" .
ex:person_alice ex:worksAt ex:company_acme .
ex:company_acme foaf:name "Acme" .
```

### Array/Collection Pattern
```json
{"tags": ["python", "graph", "rdf"]}
↓
ex:subject ex:tag "python" .
ex:subject ex:tag "graph" .
ex:subject ex:tag "rdf" .
```

### Type Inference Pattern
```json
{"age": 30, "created": "2024-04-09"}
↓
ex:subject foaf:age "30"^^xsd:integer .
ex:subject schema:dateCreated "2024-04-09"^^xsd:date .
```

## Output Formats

### RDF Turtle Format
```turtle
@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

ex:subject foaf:name "Alice" .
ex:subject foaf:age 30 .
ex:subject foaf:workplaceHomepage ex:company .
```

### N-Triples Format
```
<http://example.org/subject> <http://xmlns.com/foaf/0.1/name> "Alice" .
<http://example.org/subject> <http://xmlns.com/foaf/0.1/age> "30"^^<http://www.w3.org/2001/XMLSchema#integer> .
```

### JSON-LD Format
```json
{
  "@context": {
    "@vocab": "http://schema.org/",
    "foaf": "http://xmlns.com/foaf/0.1/"
  },
  "@type": "Person",
  "@id": "http://example.org/subject",
  "foaf:name": "Alice",
  "foaf:age": 30
}
```

### Graph JSON Format
```json
{
  "nodes": [
    {"id": "person_alice", "type": "Person", "properties": {"name": "Alice", "age": 30}},
    {"id": "company_acme", "type": "Organization", "properties": {"name": "Acme"}}
  ],
  "edges": [
    {"source": "person_alice", "target": "company_acme", "type": "worksFor"}
  ]
}
```

## Namespace Management

### Standard Vocabularies
```
foaf:     http://xmlns.com/foaf/0.1/
schema:   http://schema.org/
rdf:      http://www.w3.org/1999/02/22-rdf-syntax-ns#
rdfs:     http://www.w3.org/2000/01/rdf-schema#
owl:      http://www.w3.org/2002/07/owl#
xsd:      http://www.w3.org/2001/XMLSchema#
dbo:      http://dbpedia.org/ontology/
```

### Custom Namespaces
```yaml
namespaces:
  ex: http://example.org/
  myapp: http://myapp.example.org/
  custom: http://custom.vocabulary.org/
```

## Data Type Inference

### Type Detection
```
String values     → xsd:string
Numbers (integer) → xsd:integer
Numbers (float)   → xsd:decimal
Booleans          → xsd:boolean
ISO dates         → xsd:date / xsd:dateTime
URIs              → xsd:anyURI
```

### Literal Language Tags
```json
{"title": {"en": "Alice", "fr": "Aline"}}
↓
ex:subject rdfs:label "Alice"@en .
ex:subject rdfs:label "Aline"@fr .
```

## Execution Steps

1. **Parse JSON** – Load and validate JSON structure
2. **Infer Schema** – Detect entities and relationships
3. **Generate URIs** – Create unique identifiers for entities
4. **Build Triples** – Generate subject-predicate-object statements
5. **Manage Namespaces** – Apply namespace prefixes
6. **Deduplicate** – Remove duplicate entities
7. **Validate Output** – Check triple validity
8. **Format Output** – Generate desired output format

## Recommended Libraries

- **RDF Processing:** rdflib, oxrdflib, pyld
- **JSON Processing:** json, jsonld, python-jsonld
- **Validation:** rdflib.plugins.sparql, owlready2
- **URI Management:** URIRef, Namespace
- **Schema.org:** schema, schema-org
- **Data Type Handling:** xsd, dateutil

## Best Practices

✓ Use consistent namespace URIs  
✓ Generate meaningful entity identifiers  
✓ Normalize entity names to prevent duplicates  
✓ Use standard vocabularies (schema.org, FOAF)  
✓ Include language tags for multilingual content  
✓ Type literal values appropriately  
✓ Document custom vocabulary mappings  
✓ Validate triples before output  
✓ Handle nested structures recursively  
✓ Manage URIs consistently  

## Integration with Downstream Skills

The generated triples feed into:

- **Graph Constraint Generator** – Define constraints on triple data
- **Graph Schema Validation** – Validate against RDF schemas
- **Graph Query Optimization** – Optimize SPARQL queries
- **Knowledge Graph Construction** – Build KGs from triples
- **ETL Pipeline Generator** – Orchestrate conversion workflows

## References

See [conversion-patterns.md](references/conversion-patterns.md) for detailed JSON-to-triples conversion patterns and [example-conversions.md](examples/example-conversions.md) for complete real-world examples.

---

**Version:** 1.0.0
