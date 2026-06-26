# Entity Recognition Pipeline

## Overview

Entity recognition is the process of identifying and classifying mentions of real-world objects (people, organizations, locations, etc.) within natural language queries. This module handles the extraction and normalization of entities that will become nodes in graph queries.

## Architecture

```
Input Text
    ↓
[Tokenization & POS Tagging]
    ↓
[Named Entity Recognition]
    ↓
[Entity Classification]
    ↓
[Schema Mapping]
    ↓
Output: Classified Entities
```

## Step 1: Tokenization and Tagging

Break text into tokens and identify parts of speech:

**Input:**
```
"Find employees who work at Acme Corporation"
```

**Output (tokens with POS tags):**
```
Find (VB) employees (NNS) who (WP) work (VBP) at (IN) Acme (NNP) Corporation (NNP)
```

**POS Tags:**
- NNP: Proper noun, singular
- NNS: Noun, plural
- VB: Verb, base form
- IN: Preposition

---

## Step 2: Named Entity Recognition (NER)

Identify spans of text that represent entities:

**Common Entity Types:**

| Type | Pattern | Examples |
|------|---------|----------|
| PERSON | Proper nouns, pronouns | Alice, Bob, John Smith |
| ORGANIZATION | Corporate names, acronyms | Acme Corp, IBM, Google |
| LOCATION | Geographic locations | New York, California, London |
| PRODUCT | Product/service names | iPhone, Database, Software |
| DATE | Temporal expressions | March 2026, yesterday, 2026-03-08 |
| MONEY | Monetary amounts | $50,000, 100k, $1.5M |
| NUMBER | Numeric values | 10, 5.5, 100 |

**Example:**
```
Input: "Find employees at Acme who earn more than $60,000"

Entities:
- "Acme" → ORGANIZATION
- "$60,000" → MONEY
- "employees" → PERSON (context-specific)
```

### NER Techniques

**Rule-Based Patterns:**
```
[Capital Letter]+([Capital Letter]+)* → ORGANIZATION/PERSON
[Digit]+([,.]?[Digit]+)* → NUMBER
\$[Digit,.]+ → MONEY
```

**Dictionary Lookup:**
```
Known company names: Acme, Google, Microsoft, ...
Known locations: New York, London, Paris, ...
```

**Statistical Models:**
- BiLSTM-CRF for token classification
- Transformer-based models (BERT, RoBERTa)

---

## Step 3: Entity Classification

Map recognized entities to graph database labels:

**Classification Rules:**

```python
def classify_entity(text, entity_type, context):
    if entity_type == "ORGANIZATION":
        return "Company"
    elif entity_type == "PERSON":
        if "manager" in context or "boss" in context:
            return "Manager"
        elif "employee" in context or "worker" in context:
            return "Employee"
        else:
            return "Person"
    elif entity_type == "LOCATION":
        return "City"  # or "Country", "Region"
    # ...
```

**Context-Aware Classification:**

```
"Alice is an employee" → Person label: Employee
"Alice is a manager" → Person label: Manager
"Alice is a company" → Organization label: Company
```

---

## Step 4: Schema Mapping

Map entities to specific schema labels in the graph:

**Schema Definition Example:**
```json
{
  "nodes": [
    {"label": "Person", "properties": ["name", "age", "email"]},
    {"label": "Company", "properties": ["name", "founded_year", "industry"]},
    {"label": "City", "properties": ["name", "country", "population"]}
  ],
  "relationships": [
    {"type": "WORKS_AT", "from": "Person", "to": "Company"},
    {"type": "LOCATED_IN", "from": "Company", "to": "City"}
  ]
}
```

**Mapping Process:**

1. Extract entity text and type
2. Look up in schema
3. Find compatible node label
4. Store entity reference

**Example:**
```
Recognized: "Acme" (ORGANIZATION)
Schema lookup: ORGANIZATION → Company ✓
Result: Acme will become node with label Company

Recognized: "Alice" (PERSON)
Schema lookup: PERSON → Person ✓
Context: "works at" → Person works at Company
Result: Alice will become node with label Person
```

---

## Step 5: Property Extraction

Extract properties of entities:

**Example:**
```
"Find employees at Acme earning more than $60,000"

Entity: Acme
Properties: {name: "Acme"}

Entity: Employees
Properties: {salary > 60000}
```

### Property Patterns

| Property | Extraction Pattern | Example |
|----------|------------------|---------|
| name | "named X", "X company", quotes | "company named Acme" |
| age | "X years old", "age X" | "30 years old" |
| salary | "[comparative] X [currency]" | "more than $60k" |
| location | "in X", "at X" | "in California" |
| date | temporal expressions | "since 2020" |

---

## Step 6: Entity Linking

Link entity mentions to canonical entities in the graph:

**Challenge:**
```
"Find people who work at Acme"
vs
"Show employees at the Acme Corporation"

Both refer to the same entity but with different mentions.
```

**Resolution:**
1. Normalize entity text (lowercase, remove articles)
2. Check for known aliases
3. Perform fuzzy matching if needed
4. Link to canonical ID in database

**Example:**
```
"Acme" → Acme Corporation → canonical_id: company_123
"Acme Corp" → Acme Corporation → canonical_id: company_123
"The Acme" → Acme Corporation → canonical_id: company_123

Result: All references point to company_123
```

---

## Implementation Strategies

### Strategy 1: Rule-Based

**Pros:**
- Deterministic and interpretable
- Fast execution
- No training data needed

**Cons:**
- Limited to predefined patterns
- Manual rule maintenance

**Example:**
```python
def extract_entities(text):
    entities = []
    
    # Pattern: "[The] {NOUN} [NOUN]"
    for proper_noun_match in regex.finditer(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', text):
        entities.append(("ORGANIZATION", proper_noun_match.group()))
    
    # Pattern: "$[number]"
    for amount_match in regex.finditer(r'\$[\d,]+(?:\.\d{2})?', text):
        entities.append(("MONEY", amount_match.group()))
    
    return entities
```

### Strategy 2: Statistical (ML-Based)

**Pros:**
- Handles unseen patterns
- Adapts to domain
- Higher accuracy

**Cons:**
- Requires training data
- Slower inference
- Less interpretable

**Example:**
```python
# Using spaCy NER
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Find employees at Acme earning $60,000")

for ent in doc.ents:
    print(f"{ent.text} → {ent.label_}")
    
# Output:
# Acme → ORG
# $60,000 → MONEY
```

### Strategy 3: Hybrid

Combine rule-based and statistical approaches:

```python
def hybrid_entity_extraction(text):
    # Step 1: Rule-based for known patterns
    rule_based_entities = extract_rule_based(text)
    
    # Step 2: Statistical model for remaining text
    ml_entities = extract_with_ml(text)
    
    # Step 3: Merge and deduplicate
    all_entities = combine_results(rule_based_entities, ml_entities)
    
    return all_entities
```

---

## Handling Edge Cases

### Ambiguous Entities

**Challenge:**
```
"Apple launched a new product"
- Is "Apple" a company or fruit?
```

**Solution:**
```
Use contextual clues:
- "launched" suggests Company context
- Look at schema: Company can "launch", Fruit cannot
- Result: Map to Company label
```

### Nested Entities

**Challenge:**
```
"The CEO of Acme Corporation"
- "Acme Corporation" is entity
- "CEO" is role, not separate entity
```

**Solution:**
```
Use hierarchy:
- Recognize "Acme Corporation" as primary entity (ORGANIZATION)
- "CEO" is a property/role, not separate entity
```

### Pronoun Resolution

**Challenge:**
```
"Alice works at Acme. She manages the engineering team."
- "She" refers to Alice
```

**Solution:**
```
Coreference resolution:
1. Find pronouns ("She")
2. Look back to find likely referent ("Alice")
3. Link "She" to Alice entity
```

### Multi-word Entities

**Challenge:**
```
"New York" is a single entity, not two
```

**Solution:**
```
Use phrase-level recognition:
- Recognize "New York" as complete location entity
- Don't split on word boundaries
```

---

## Quality Metrics

### Precision
```
Correct entities / All predicted entities
```

### Recall
```
Correct entities / All actual entities
```

### F1-Score
```
Harmonic mean of precision and recall
```

### Benchmark on Standard Datasets

- CoNLL 2003 NER
- OntoNotes
- Domain-specific benchmarks

---

## Best Practices

✓ Normalize entity text (lowercase, remove special characters for matching)  
✓ Maintain entity disambiguation log  
✓ Use schema constraints to validate entities  
✓ Handle abbreviations and aliases  
✓ Test with domain-specific examples  
✓ Monitor entity extraction quality  
✓ Update entity dictionaries regularly  

---

## See Also

- [Relationship Extraction](relationship-extraction.md)
- [Query Patterns Reference](query-patterns.md)
- [Schema Validation](../../../graph_modeling_and_schema_design/graph-schema-validation/SKILL.md)

