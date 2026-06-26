---
name: mapping_dsl_builder
title: Mapping DSL Builder
description: Generate declarative mapping rules that transform structured data sources into graph triples or nodes using a domain-specific mapping language similar to R2RML.
category: data-ingestion
tags:
  - mapping-rules
  - dsl-generation
  - r2rml
  - data-transformation
  - relational-to-graph
  - etl-configuration
  - declarative-mappings
  - schema-mapping
  - transformation-rules
  - developer-tools
version: 1.0.0
author: community
license: MIT
metadata:
  {"openclaw":{"emoji":"🗺️","homepage":"https://clawhub.com"}}
---

# Mapping DSL Builder

**Generate declarative mapping rules for transforming data into graph structures.**

This skill creates **domain-specific language (DSL) mappings** that define how data fields from structured sources such as databases, CSV files, JSON, or APIs should be transformed into **nodes, relationships, and triples** for graph databases or knowledge graphs. The mapping language functions similarly to **R2RML**, the standard for relational-to-RDF mappings.

## Quick Start

### Use When
- Defining mappings between structured datasets and graph models
- Creating declarative transformation rules
- Converting relational schemas into RDF triples
- Building graph ingestion mapping specifications
- Generating reusable data-to-graph mapping configurations
- Standardizing ETL transformation definitions

### Inputs
- Source schema definitions (database, CSV, JSON, API)
- Entity type specifications
- Column/property definitions
- Foreign key relationships
- Identifier specifications
- Mapping rules and transformations
- Target graph schema

### Outputs
- Custom Mapping DSL specifications
- R2RML (RDF Mapping Language) definitions
- YAML mapping configurations
- JSON mapping specifications
- Property graph mappings
- Executable mapping configurations
- Data transformation documentation

## Example

**Input Database Schema:**
```sql
CREATE TABLE employee (
  id INT,
  name VARCHAR(255),
  email VARCHAR(255),
  company_id INT
);

CREATE TABLE company (
  id INT,
  name VARCHAR(255),
  industry VARCHAR(100)
);
```

**Generated Mapping DSL:**
```yaml
mapping: EmployeeMapping
version: 1.0

source:
  type: database
  table: employee
  connection: postgresql://localhost/company_db

entity:
  type: Person
  identifier: id
  uri_template: "http://example.org/person/{id}"

properties:
  - source: name
    target: http://xmlns.com/foaf/0.1/name
    type: string
  - source: email
    target: http://xmlns.com/foaf/0.1/mbox
    type: string

relationships:
  - name: WORKS_AT
    source: company_id
    target: Company
    target_identifier: id
```

## Mapping DSL Architecture

### 1. Source Definition

**Purpose:** Specify where data comes from

**Types Supported:**
- **Database** - SQL databases (PostgreSQL, MySQL, Oracle)
- **CSV** - Comma/delimiter-separated files
- **JSON** - JSON files or documents
- **API** - REST API endpoints
- **Streaming** - Real-time data streams

**Configuration:**
```yaml
source:
  type: database|csv|json|api|stream
  connection_string: connection_details
  table_or_location: specification
  format: format_options
```

### 2. Entity Mapping

**Purpose:** Define how records map to graph entities

**Components:**
- **Type** - Entity type/label (Person, Organization, etc.)
- **Identifier** - Column(s) that uniquely identify records
- **URI Template** - Pattern for generating entity URIs
- **Properties** - Attributes to include

**Configuration:**
```yaml
entity:
  type: EntityType
  identifier: id_column
  uri_template: "http://example.org/type/{id}"
  namespace: http://example.org/
```

### 3. Property Mapping

**Purpose:** Map source attributes to graph properties

**Details:**
- Source column name
- Target property URI
- Data type
- Transformations (optional)
- Default values (optional)

**Configuration:**
```yaml
properties:
  - source: database_column
    target: http://schema.org/propertyName
    type: string|integer|date
    transformation: function_name
    required: true|false
```

### 4. Relationship Mapping

**Purpose:** Define relationships between entities

**Details:**
- Relationship name/type
- Source column (foreign key)
- Target entity
- Cardinality
- Direction

**Configuration:**
```yaml
relationships:
  - name: RELATIONSHIP_TYPE
    source: foreign_key_column
    target: TargetEntity
    target_identifier: target_id
    cardinality: "1..1"|"1..*"|"*..1"|"*..*"
    direction: forward|backward|bidirectional
```

## Mapping Patterns

### Database Mapping Pattern
```yaml
Pattern: Map relational table to graph entity

source:
  type: database
  table: employee
relationships:
  - name: WORKS_AT
    source: company_id (foreign key)
    target: Company entity
```

### CSV Mapping Pattern
```yaml
Pattern: Map CSV columns to graph properties

source:
  type: csv
  file: data/employees.csv
  delimiter: ","
entity:
  identifier: person_id (unique column)
properties:
  - source: name
    target: foaf:name
```

### JSON Mapping Pattern
```yaml
Pattern: Map JSON properties to graph structure

source:
  type: json
  path: $.employees[*]
entity:
  identifier: $.id
properties:
  - source: $.name
    target: http://example.org/name
```

### Nested Object Mapping Pattern
```yaml
Pattern: Handle nested structures

source:
  type: json
  path: $.employees[*]
relationships:
  - name: HAS_ADDRESS
    source: $.address (nested object)
    target: Address
    inline: true
```

## Output Formats

### Custom Mapping DSL

```yaml
mapping: PersonMapping
version: 1.0

source:
  type: csv
  file: people.csv

entity:
  type: Person
  identifier: person_id

properties:
  - source: name
    target: foaf:name
  - source: email
    target: foaf:mbox

relationships:
  - name: WORKS_AT
    source: company_id
    target: Company
```

### R2RML Format

```turtle
@prefix rr: <http://www.w3.org/ns/r2rml#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix ex: <http://example.org/> .

ex:EmployeeMapping a rr:TriplesMap ;
  rr:logicalTable [ rr:tableName "employee" ] ;
  rr:subjectMap [
    rr:template "http://example.org/person/{id}" ;
    rr:class foaf:Person
  ] ;
  rr:predicateObjectMap [
    rr:predicate foaf:name ;
    rr:objectMap [ rr:column "name" ]
  ] ;
  rr:predicateObjectMap [
    rr:predicate foaf:workplaceHomepage ;
    rr:objectMap [
      rr:parentTriplesMap ex:CompanyMapping ;
      rr:joinCondition [ rr:child "company_id" ; rr:parent "id" ]
    ]
  ] .
```

### YAML Format

```yaml
version: 1.0
mappings:
  - name: PersonMapping
    source:
      type: database
      table: person
    entity:
      type: Person
      id: person_id
    properties:
      name: name
      email: email_address
    relationships:
      works_at:
        target: Company
        foreign_key: company_id
```

## Data Type Support

### Supported Types
- **string** - Text data
- **integer** - Whole numbers
- **decimal** - Floating point numbers
- **boolean** - True/false values
- **date** - Date values (YYYY-MM-DD)
- **datetime** - Date and time
- **uri** - Uniform resource identifiers
- **custom** - User-defined types

### Type Mapping
```yaml
Relational → RDF Type Mapping
INTEGER → xsd:integer
VARCHAR → xsd:string
DATE → xsd:date
DECIMAL → xsd:decimal
BOOLEAN → xsd:boolean
```

## Transformation Functions

### Built-in Transformations
```
concat(field1, field2)    - Concatenate fields
uppercase(field)          - Convert to uppercase
lowercase(field)          - Convert to lowercase
substring(field, 0, 5)    - Extract substring
replace(field, old, new)  - Replace values
regex(field, pattern)     - Regex matching
split(field, delimiter)   - Split string
trim(field)               - Remove whitespace
```

## Execution Steps

1. **Analyze Source Schema** – Detect structure and data types
2. **Identify Entities** – Find key identifiers
3. **Detect Relationships** – Recognize foreign keys
4. **Map Properties** – Associate columns to properties
5. **Generate URIs** – Create entity identifiers
6. **Define Transformations** – Apply any conversions
7. **Validate Mapping** – Check for consistency
8. **Generate Output** – Produce mapping specifications

## Recommended Libraries

- **Mapping Processing:** rdflib, r2rml-processor, morph-kgc
- **DSL Generation:** pyparsing, lark, textx
- **Schema Analysis:** sqlalchemy, pandas, jsonschema
- **RDF Generation:** rdflib, sparql-client
- **YAML/Config:** pyyaml, toml, configparser
- **Database:** sqlalchemy, psycopg2, pymongo

## Best Practices

✓ Use consistent URI templates  
✓ Choose meaningful identifiers  
✓ Document mapping rationale  
✓ Normalize property names  
✓ Handle missing values explicitly  
✓ Test mappings with sample data  
✓ Version mapping configurations  
✓ Document transformations  
✓ Validate schemas before mapping  
✓ Keep mappings reusable  

## Integration with Downstream Skills

Generated mappings are used by:

- **ETL Pipeline Generator** – Execute mappings in pipelines
- **JSON to Triples Converter** – Transform JSON using mappings
- **CSV Graph Loader Generator** – Load CSV with defined mappings
- **Graph Schema Validation** – Validate mapped data
- **Graph Constraint Generator** – Apply constraints to mapped data

## References

See [mapping-patterns.md](references/mapping-patterns.md) for detailed mapping design patterns and [example-mappings.md](examples/example-mappings.md) for complete real-world examples.

---

**Version:** 1.0.0
