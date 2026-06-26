# JSON to Triples Conversion Patterns

This guide provides patterns for converting JSON documents into RDF triples and semantic formats.

## URI Generation Patterns

### Simple Subject Pattern

```
Pattern: Generate subject URI from entity identifier

Input: {"id": "alice_001", "name": "Alice"}
Output: ex:person_alice_001

Rules:
  - Use entity type + identifier
  - Format: ex:entity_type_id
  - Ensure URI uniqueness
```

### Hashed Identifier Pattern

```
Pattern: Generate URI from object hash when ID unavailable

Input: {"name": "Alice", "city": "New York"}
Output: ex:person_7a2f3c9d (hash of content)

Use case: When unique ID doesn't exist in JSON
```

### Name-Based URI Pattern

```
Pattern: Generate URI from entity name

Input: {"name": "Alice Johnson"}
Output: ex:person_alice_johnson

Rules:
  - Lowercase and slug format
  - Replace spaces with underscores
  - Remove special characters
```

---

## Property Mapping Patterns

### Direct Property Mapping

```
Pattern: Map JSON key directly to RDF predicate

Input: {"name": "Alice", "age": 30}
↓
ex:person foaf:name "Alice" .
ex:person foaf:age 30 .

Mapping:
  name → foaf:name
  age → foaf:age
```

### Custom Predicate Mapping

```yaml
Pattern: Custom key-to-predicate mapping

Mappings:
  "email" → "foaf:mbox"
  "phone" → "foaf:phone"
  "company" → "schema:worksFor"
  "created_at" → "dcterms:created"

Input: {"email": "alice@example.com"}
Output: ex:person foaf:mbox <mailto:alice@example.com> .
```

### Nested Property Flattening

```
Pattern: Flatten nested properties to triples

Input: {
  "user": {
    "address": {
      "city": "New York",
      "zip": "10001"
    }
  }
}

Output:
ex:user_123 schema:city "New York" .
ex:user_123 schema:zip "10001" .
```

---

## Relationship Extraction Patterns

### Direct Relationship Pattern

```
Pattern: Extract relationships from nested objects

Input: {
  "person": "Alice",
  "company": "Acme"
}

Output:
ex:person_alice schema:worksFor ex:company_acme .

Rules:
  - Nested object → relationship
  - Parent entity → subject
  - Nested entity → object
  - Key name → relationship type
```

### Array-to-Multiple-Triples Pattern

```
Pattern: Convert JSON arrays to multiple triples

Input: {
  "person": "Alice",
  "skills": ["Python", "GraphQL", "RDF"]
}

Output:
ex:person_alice schema:skill "Python" .
ex:person_alice schema:skill "GraphQL" .
ex:person_alice schema:skill "RDF" .
```

### Many-to-Many Relationship Pattern

```
Pattern: Represent many-to-many relationships

Input: {
  "author": "Alice",
  "papers": [
    {"id": "p1", "title": "Paper 1"},
    {"id": "p2", "title": "Paper 2"}
  ]
}

Output:
ex:author_alice foaf:made ex:paper_p1 .
ex:author_alice foaf:made ex:paper_p2 .
ex:paper_p1 dcterms:title "Paper 1" .
ex:paper_p2 dcterms:title "Paper 2" .
```

---

## Data Type Inference Patterns

### Automatic Type Detection

```
Pattern: Infer data types from JSON values

Input: {
  "name": "Alice",        → string
  "age": 30,              → integer
  "height": 5.6,          → decimal
  "active": true,         → boolean
  "date": "2024-04-09"    → date
}

Output:
ex:person foaf:name "Alice"^^xsd:string .
ex:person foaf:age "30"^^xsd:integer .
ex:person ex:height "5.6"^^xsd:decimal .
ex:person ex:active "true"^^xsd:boolean .
ex:person dcterms:created "2024-04-09"^^xsd:date .
```

### Literal Language Tagging

```
Pattern: Add language tags for multilingual content

Input: {
  "titles": {
    "en": "The Title",
    "fr": "Le Titre",
    "es": "El Título"
  }
}

Output:
ex:resource rdfs:label "The Title"@en .
ex:resource rdfs:label "Le Titre"@fr .
ex:resource rdfs:label "El Título"@es .
```

### URI Value Detection

```
Pattern: Detect and preserve URI values

Input: {
  "website": "https://example.com",
  "orcid": "https://orcid.org/0000-0001-2345-6789"
}

Output:
ex:person foaf:homepage <https://example.com> .
ex:person ex:orcid <https://orcid.org/0000-0001-2345-6789> .
```

---

## Namespace Management Patterns

### Standard Vocabulary Pattern

```yaml
Pattern: Use standard RDF vocabularies

Namespaces:
  foaf: http://xmlns.com/foaf/0.1/
  schema: http://schema.org/
  dcterms: http://purl.org/dc/terms/
  xsd: http://www.w3.org/2001/XMLSchema#
  rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#

Benefits:
  - Semantic clarity
  - Interoperability
  - Standard predicates
```

### Custom Namespace Pattern

```yaml
Pattern: Define custom domain-specific namespaces

namespaces:
  myapp: http://myapp.example.org/
  mydomain: http://mydomain.example.org/
  custom: http://custom.vocab.example.org/

Usage:
ex:person mydomain:customProperty "value" .
```

### Namespace Prefix Mapping

```yaml
Pattern: Map external properties to internal namespace

Mappings:
  "schema.org/name" → "foaf:name"
  "schema.org/email" → "foaf:mbox"
  "company/org_id" → "ex:companyId"

Benefits:
  - Standardization
  - Normalization
  - URI consolidation
```

---

## Entity Deduplication Patterns

### Exact Match Deduplication

```
Pattern: Merge entities with identical properties

Input:
{
  "people": [
    {"id": "p1", "name": "Alice", "email": "alice@example.com"},
    {"id": "p2", "name": "Alice", "email": "alice@example.com"}
  ]
}

Processing:
  - Detect duplicate email
  - Same name
  - Merge to single entity

Output:
ex:person_alice foaf:name "Alice" .
ex:person_alice foaf:mbox <mailto:alice@example.com> .
```

### Fuzzy Matching Deduplication

```
Pattern: Merge similar entities (e.g., name variations)

Input:
{
  "people": [
    {"name": "Alice Johnson"},
    {"name": "Alice J."},
    {"name": "A. Johnson"}
  ]
}

Similarity Threshold: > 0.85

Output:
Single merged entity with all names
ex:person_alice foaf:name "Alice Johnson" ;
              foaf:name "Alice J." ;
              foaf:name "A. Johnson" .
```

### Reference-Based Deduplication

```
Pattern: Link and consolidate entities by ID

Input:
{
  "employees": [
    {"emp_id": "E001", "name": "Alice", "salary": 100000},
    {"emp_id": "E001", "name": "Alice", "salary": 105000}
  ]
}

Merge Strategy:
  - Same emp_id → same entity
  - Keep latest values
  - Merge non-conflicting properties

Output:
ex:employee_E001 foaf:name "Alice" ;
                 schema:salary 105000 .
```

---

## Vocabulary Selection Patterns

### Schema.org Pattern

```
Pattern: Use schema.org for structured data

Vocabularies:
  Person → schema:Person
  name → schema:name
  email → schema:email
  organization → schema:Organization
  worksFor → schema:worksFor

Benefits:
  - Wide adoption
  - SEO friendly
  - Well-documented
```

### FOAF Pattern

```
Pattern: Use FOAF for social/network data

Vocabularies:
  Person → foaf:Person
  name → foaf:name
  email → foaf:mbox
  knows → foaf:knows
  based_near → foaf:based_near

Benefits:
  - Social network focused
  - Relationship emphasis
  - Community adoption
```

### Domain-Specific Vocabulary Pattern

```
Pattern: Create domain-specific vocabularies

Example (Academic):
  Author → author:Author
  Paper → author:Paper
  CitedBy → author:citedBy
  ResearchArea → author:ResearchArea

Benefits:
  - Domain precision
  - Specific relationships
  - Custom semantics
```

---

## Output Format Patterns

### Turtle Format Pattern

```turtle
Pattern: Generate human-readable RDF Turtle

@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix schema: <http://schema.org/> .

ex:person_alice a foaf:Person ;
  foaf:name "Alice" ;
  foaf:mbox <mailto:alice@example.com> ;
  schema:jobTitle "Engineer" .

Benefits:
  - Human readable
  - Compact
  - Comment support
```

### N-Triples Format Pattern

```
Pattern: Generate line-based N-Triples

<http://example.org/person_alice> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
<http://example.org/person_alice> <http://xmlns.com/foaf/0.1/name> "Alice" .

Benefits:
  - Simple parsing
  - Line-based processing
  - Direct storage
```

### JSON-LD Format Pattern

```json
Pattern: Generate JSON-LD for web integration

{
  "@context": "http://schema.org/",
  "@type": "Person",
  "name": "Alice",
  "email": "alice@example.com"
}

Benefits:
  - Web-native
  - JSON familiar
  - Semantic context
```

---

## Error Handling Patterns

### Missing Value Pattern

```
Pattern: Handle missing/null values

Strategies:
  - Skip property: Don't create triple
  - Default value: Use empty string or null
  - Error handling: Log and continue
  - Validation: Mark as invalid

Input: {"name": null, "age": 30}
Output: ex:person foaf:age 30 .
        (name triple skipped)
```

### Invalid URI Pattern

```
Pattern: Handle invalid characters in URIs

Strategies:
  - Encode special characters
  - URL encode: %20 for space
  - Slug format: lowercase, hyphenate
  - Hash: Use hash for complex values

Example:
  "Alice Johnson" → "alice-johnson"
  "Alice O'Brien" → "alice-obrien"
  "alice@example.com" → "alice%40example.com"
```

### Type Mismatch Pattern

```
Pattern: Handle unexpected data types

Strategies:
  - Type conversion: Attempt safe conversion
  - Default type: Use string as fallback
  - Validation: Mark as error
  - Logging: Record type mismatch

Example:
  age: "thirty" (string) → log error, skip
  age: "30" (string) → convert to integer
```

---

## Best Practices

✓ Use consistent namespace URIs  
✓ Choose appropriate vocabularies  
✓ Generate meaningful entity identifiers  
✓ Handle nested structures recursively  
✓ Implement entity deduplication  
✓ Type literal values appropriately  
✓ Include language tags for i18n  
✓ Validate generated triples  
✓ Document custom mappings  
✓ Test with real data  

---

See [example-conversions.md](../examples/example-conversions.md) for complete JSON-to-triples conversion examples.


