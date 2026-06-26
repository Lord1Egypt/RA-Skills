# Mapping DSL Design Patterns

This guide provides patterns for designing and implementing mapping DSL configurations.

## Source Definition Patterns

### Database Source Pattern

```yaml
Pattern: Connect to SQL database

source:
  type: database
  connection_string: "postgresql://user:pass@host:port/database"
  dialect: postgresql|mysql|oracle|tsql
  query: "SELECT * FROM table_name"
  
Supports:
  - PostgreSQL
  - MySQL
  - Oracle
  - SQL Server
  - MariaDB
```

### CSV Source Pattern

```yaml
Pattern: Read CSV file

source:
  type: csv
  file: "path/to/data.csv"
  delimiter: ","
  quote_char: "\""
  encoding: utf-8
  skip_rows: 1
  header_row: 1

Options:
  - Tab-separated
  - Custom delimiters
  - Different encodings
  - Quoted fields
```

### JSON Source Pattern

```yaml
Pattern: Parse JSON file or API

source:
  type: json
  location: "file.json" OR "https://api.example.com/data"
  path: "$.data[*]"  # JSONPath
  format: "array" | "object" | "nested"
  authentication: 
    type: bearer|basic|oauth2
    credentials: ...

Supports:
  - Local files
  - HTTP APIs
  - Streaming
  - Nested structures
```

### API Source Pattern

```yaml
Pattern: Connect to REST API

source:
  type: api
  endpoint: "https://api.example.com/users"
  method: GET|POST
  headers:
    Authorization: "Bearer token"
  pagination:
    type: offset|cursor|page
    parameter: page
    size: 100
  
Supports:
  - Basic auth
  - OAuth2
  - API keys
  - Pagination
  - Rate limiting
```

---

## Entity Mapping Patterns

### Simple Entity Pattern

```yaml
Pattern: Map single entity type

entity:
  type: http://schema.org/Person
  identifier: id
  uri_template: "http://example.org/person/{id}"
  
Single record → Single entity
ID → Entity URI
```

### Composite Identifier Pattern

```yaml
Pattern: Use multiple columns as identifier

entity:
  identifier:
    columns:
      - first_name
      - last_name
    separator: "-"
  uri_template: "http://example.org/person/{first_name}_{last_name}"

Combines: first_name + last_name → Unique ID
```

### Hash-Based Identifier Pattern

```yaml
Pattern: Generate identifier from hash

entity:
  identifier:
    type: hash
    columns:
      - field1
      - field2
    algorithm: md5|sha256
  uri_template: "http://example.org/entity/{hash}"

Use case: Unstable or missing IDs
```

### Namespace-Based Pattern

```yaml
Pattern: Use namespace prefix in URI

entity:
  namespace: "http://example.org/people/"
  identifier: person_id
  uri_template: "{namespace}{id}"

Result: http://example.org/people/123
```

---

## Property Mapping Patterns

### Direct Property Mapping

```yaml
Pattern: Simple column to property mapping

property:
  source_column: database_column
  target_predicate: http://schema.org/name
  datatype: xsd:string

One column → One property
```

### Transformed Property Pattern

```yaml
Pattern: Apply transformation to property value

property:
  source_column: birth_date
  target_predicate: foaf:age
  transformation:
    function: calculate_age
    parameters: [birth_date, today]
  datatype: xsd:integer

Applies: function(value) → transformed value
```

### Concatenated Property Pattern

```yaml
Pattern: Combine multiple columns

property:
  source_columns:
    - first_name
    - last_name
  transformation: concat
  separator: " "
  target_predicate: foaf:name

Result: "John Doe" from first_name + last_name
```

### Conditional Property Pattern

```yaml
Pattern: Include property based on condition

property:
  source_column: status
  target_predicate: foaf:currentProject
  condition:
    column: employment_status
    value: "active"

Include: Only if employment_status = "active"
```

### Language-Tagged Property Pattern

```yaml
Pattern: Add language tags to literals

property:
  source_column: description
  target_predicate: rdfs:comment
  language_tag:
    source_column: language_code
    default: "en"

Result: "Description"@en
```

---

## Relationship Mapping Patterns

### Foreign Key Relationship Pattern

```yaml
Pattern: Map foreign key to relationship

relationship:
  name: WORKS_FOR
  source_column: company_id
  target_entity: Company
  target_identifier: company_id
  predicate: http://schema.org/worksFor

Maps: employee.company_id → company.company_id
Creates: employee -[WORKS_FOR]-> company
```

### Multi-Column Relationship Pattern

```yaml
Pattern: Join on multiple columns

relationship:
  name: HAS_ROLE
  source_columns:
    - user_id
    - role_id
  target_entity: Role
  target_columns:
    - user_id
    - role_id
  predicate: ex:hasRole

Joins on: user_id AND role_id
```

### Implicit Relationship Pattern

```yaml
Pattern: Create relationship from value

relationship:
  name: LOCATED_IN
  source_column: city
  target_entity: Location
  target_identifier_value: city
  predicate: http://schema.org/location

Matches: city value to Location.name
```

### Inverse Relationship Pattern

```yaml
Pattern: Reverse relationship direction

relationship:
  name: EMPLOYED_BY
  source_column: company_id
  target_entity: Company
  direction: inverse
  predicate: http://schema.org/hasEmployee

Reverses: employee.company -[WORKS_FOR]->
          company -[HAS_EMPLOYEE]-> employee
```

### Cardinality-Based Relationship Pattern

```yaml
Pattern: Define relationship cardinality

relationship:
  name: TEACHES
  source_column: professor_id
  target_entity: Course
  cardinality: "1..*"  # One professor teaches many courses
  
Cardinalities:
  "1..1"   - One to one
  "1..*"   - One to many
  "*..1"   - Many to one
  "*..*"   - Many to many
```

---

## Data Type Mapping Patterns

### Basic Type Mapping

```yaml
Pattern: Map source type to RDF type

Database Type → RDF Type
INT            → xsd:integer
VARCHAR        → xsd:string
DATE           → xsd:date
DECIMAL        → xsd:decimal
BOOLEAN        → xsd:boolean
TIMESTAMP      → xsd:dateTime
```

### Custom Type Pattern

```yaml
Pattern: Define custom type mapping

property:
  source_column: custom_field
  source_datatype: custom_type
  target_datatype: xsd:string
  transformation: custom_serializer

Maps: custom_type → standard RDF type
```

### URI Type Pattern

```yaml
Pattern: Handle URI/URL columns

property:
  source_column: website_url
  target_predicate: foaf:homepage
  datatype: xsd:anyURI

Preserves: Full URI value
```

---

## Transformation Patterns

### String Transformation Pattern

```yaml
Pattern: Transform string values

transformations:
  - name: uppercase
    function: upper()
    input: field_name
  - name: trim
    function: trim()
  - name: replace
    function: replace(old, new)
    parameters: ["_", "-"]

Operations:
  - Case conversion
  - Whitespace handling
  - Character replacement
  - Substring extraction
```

### Date Transformation Pattern

```yaml
Pattern: Transform date values

transformation:
  source_format: "MM/DD/YYYY"
  target_format: "YYYY-MM-DD"
  function: parse_date
  
Converts: "03/15/2020" → "2020-03-15"
```

### Calculation Transformation Pattern

```yaml
Pattern: Calculate values

transformation:
  function: calculate_age
  source_column: birth_date
  parameters: [current_date]
  
Calculates: age from birth_date
```

### Lookup Transformation Pattern

```yaml
Pattern: Use lookup table

transformation:
  function: lookup
  table: code_mapping
  key_column: code
  value_column: description
  
Maps: code → description from table
```

---

## Validation Patterns

### Required Field Pattern

```yaml
validation:
  required_fields:
    - person_id
    - name
  on_missing: skip_record | error | default_value

Checks: Fields are present
Action: Skip or error if missing
```

### Data Type Validation Pattern

```yaml
validation:
  datatype_checks:
    - field: age
      expected_type: integer
      range: [0, 150]
  on_error: coerce | skip | error

Validates: Type and range
```

### Uniqueness Pattern

```yaml
validation:
  unique_fields:
    - email
    - person_id
  on_duplicate: skip | error | merge

Ensures: No duplicate values
```

---

## Advanced Patterns

### Nested Document Mapping

```yaml
Pattern: Map nested JSON/XML structures

mapping:
  source: json
  path: $.employees[*]
  
  relationships:
    - name: HAS_ADDRESS
      source_path: $.address
      inline: true (flatten) | false (separate entity)

Handles: Nested objects as inline properties or separate entities
```

### Conditional Mapping Pattern

```yaml
Pattern: Include mappings based on conditions

mapping:
  condition:
    field: record_type
    value: "employee"
  
  properties:
    - source_column: salary
      include_if: is_active = true

Applies: Mappings only when condition is met
```

### Inheritance Mapping Pattern

```yaml
Pattern: Extend base mapping

base_mapping: PersonMapping

extends:
  additional_properties:
    - source_column: employment_status
  additional_relationships:
    - name: EMPLOYED_BY
      source_column: company_id
```

---

## Best Practices

✓ Use meaningful entity identifiers  
✓ Define consistent URI templates  
✓ Document all transformations  
✓ Handle missing values explicitly  
✓ Validate schema before mapping  
✓ Test with sample data  
✓ Version mapping configurations  
✓ Keep mappings modular and reusable  
✓ Use standard vocabularies  
✓ Monitor mapping execution  

---

See [example-mappings.md](../examples/example-mappings.md) for complete mapping DSL implementation examples.


