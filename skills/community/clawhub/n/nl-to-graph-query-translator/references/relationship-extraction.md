# Relationship Extraction

## Overview

Relationship extraction identifies and classifies the semantic connections between entities mentioned in natural language text. This module converts verb phrases and prepositions into graph relationship types.

## Relationship Extraction Pipeline

```
Input Text
    ↓
[Sentence Segmentation]
    ↓
[Entity Identification]
    ↓
[Verb/Predicate Extraction]
    ↓
[Relationship Classification]
    ↓
[Direction & Properties Assignment]
    ↓
Output: Relationships
```

---

## Step 1: Identify Relation Patterns

### Explicit Relations (Verbs)

Direct action verbs that denote relationships:

**Example:**
```
"Alice works at Acme"
└─ Verb: "works at" → Relationship: WORKS_AT
```

**Common patterns:**
```
[Entity1] [VERB] [Entity2]

- "Alice manages Bob" → MANAGES
- "Alice knows Bob" → KNOWS
- "Alice purchased Product" → PURCHASED
```

### Implicit Relations (Prepositions)

Spatial or semantic relationships indicated by prepositions:

**Example:**
```
"Acme is located in New York"
└─ Preposition: "in" → Relationship: LOCATED_IN
```

**Common patterns:**
```
[Entity1] [PREP] [Entity2]

- "Company in City" → LOCATED_IN
- "Product of Company" → MADE_BY
- "Manager of Team" → MANAGES
```

### Nominal Relations (Nouns)

Implicit relationships expressed through noun phrases:

**Example:**
```
"The CEO of Acme is Alice"
└─ Noun: "CEO" → Implicit relationship: MANAGES/LEADS
```

---

## Step 2: Verb Phrase Extraction

### Simple Verbs

Single-word verbs:
```
"Alice works at Acme" → works_at
"Bob knows Alice" → knows
"Company owns Product" → owns
```

### Phrasal Verbs

Multi-word verb combinations:
```
"Alice works for Acme" → works_for
"Company takes over Competitor" → takes_over
"Person reports to Manager" → reports_to
```

### Verb + Preposition Combinations

```
"Alice works at Acme" → work + at = WORKS_AT
"Company competes in Market" → compete + in = COMPETES_IN
"Employee reports to Manager" → report + to = REPORTS_TO
```

---

## Step 3: Relationship Mapping

Map linguistic expressions to graph relationship types:

### Mapping Table

| Linguistic Expression | Relationship Type | Direction | Schema |
|----------------------|------------------|-----------|--------|
| "works at" | WORKS_AT | Person → Company | Person-WORKS_AT-Company |
| "works for" | WORKS_FOR | Person → Company | Person-WORKS_FOR-Company |
| "manages" | MANAGES | Person → Person | Manager-MANAGES-Employee |
| "reports to" | REPORTS_TO | Person → Person | Employee-REPORTS_TO-Manager |
| "knows" | KNOWS | Person ↔ Person | Person-KNOWS-Person |
| "located in" | LOCATED_IN | Company → City | Company-LOCATED_IN-City |
| "in" | LOCATED_IN | Entity → Location | Entity-LOCATED_IN-Location |
| "owns" | OWNS | Person → Company | Person-OWNS-Company |
| "founded" | FOUNDED | Person → Company | Person-FOUNDED-Company |
| "purchased" | PURCHASED | Person/Org → Product | Buyer-PURCHASED-Product |
| "created" | CREATED | Person → Product | Person-CREATED-Product |
| "part of" | PART_OF | Entity → Entity | Child-PART_OF-Parent |

---

## Step 4: Direction Assignment

Determine if relationships are directed or undirected:

### Directed Relationships

Clear subject → object direction:

```
"Alice works at Acme"
Direction: Alice (source) → Acme (target)
Type: WORKS_AT
```

**Indicators:**
- Active voice verbs ("manages", "owns")
- Prepositions with clear source/target ("in", "at", "by")
- Agent → Patient pattern

### Undirected Relationships

Symmetric relationships without clear directionality:

```
"Alice knows Bob"
Direction: Alice ↔ Bob (bidirectional)
Type: KNOWS
```

**Indicators:**
- Mutual knowledge verbs ("knows", "meets")
- Symmetric prepositions ("with", "between")
- Reciprocal relationships

### Reverse Relationships

Sometimes both directions are useful:

```
Forward: Company EMPLOYS Person
Reverse: Person EMPLOYED_BY Company
```

---

## Step 5: Relationship Properties

Extract additional metadata about relationships:

### Temporal Properties

```
"Alice worked at Acme from 2020 to 2025"

Relationship: WORKS_AT
Properties:
  - start_date: 2020-01-01
  - end_date: 2025-12-31
  - duration: 5 years
```

### Quantitative Properties

```
"Alice owns 15% of Acme"

Relationship: OWNS
Properties:
  - percentage: 15
  - shares: 1500
```

### Qualitative Properties

```
"Alice strongly disagrees with Bob"

Relationship: DISAGREES_WITH
Properties:
  - strength: "strong"
  - sentiment: "negative"
```

---

## Extraction Techniques

### Technique 1: Pattern-Based Rules

Define regex patterns for common relationship expressions:

```python
def extract_relationships_rule_based(text):
    relationships = []
    
    patterns = [
        # Pattern: [Entity1] works at [Entity2]
        {
            "pattern": r"(\w+)\s+works\s+at\s+(\w+)",
            "relation_type": "WORKS_AT",
            "direction": "forward"
        },
        # Pattern: [Entity1] located in [Entity2]
        {
            "pattern": r"(\w+)\s+located\s+in\s+(\w+)",
            "relation_type": "LOCATED_IN",
            "direction": "forward"
        },
    ]
    
    for pattern_def in patterns:
        for match in regex.finditer(pattern_def["pattern"], text):
            relationships.append({
                "entity1": match.group(1),
                "entity2": match.group(2),
                "type": pattern_def["relation_type"],
                "direction": pattern_def["direction"]
            })
    
    return relationships
```

**Pros:**
- Fast and deterministic
- Easy to understand and maintain
- No training data required

**Cons:**
- Limited to predefined patterns
- Doesn't handle variations well

### Technique 2: Dependency Parsing

Use syntactic parse trees to identify relationships:

```
"Alice works at Acme"

Parse tree:
         S
       / | \
      NP VP  PP
      |  |   |
    Alice works at Acme
    
Dependencies:
- nsubj: Alice → works (subject)
- prep: works → at (prepositional phrase)
- pobj: at → Acme (prepositional object)

Relationship extraction:
- Entity1: Alice (nsubj)
- Verb: works
- Entity2: Acme (pobj)
- Relation type: WORKS_AT
```

**Implementation with spaCy:**
```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Alice works at Acme")

for token in doc:
    if token.dep_ == "nsubj":
        subject = token.text
    elif token.pos_ == "VERB":
        verb = token.text
    elif token.dep_ == "pobj":
        obj = token.text

print(f"{subject} -[{verb}]-> {obj}")
```

**Pros:**
- Handles syntactic variations
- More robust than simple regex

**Cons:**
- Requires NLP pipeline
- Slower than pattern matching

### Technique 3: Machine Learning

Train a classifier to recognize relationship types:

```python
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer

# Training data
texts = [
    "Alice works at Acme",
    "Bob manages the team",
    "Product purchased by Company",
]
labels = ["WORKS_AT", "MANAGES", "PURCHASED"]

# Feature extraction
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Train classifier
clf = SVC(kernel='linear')
clf.fit(X, labels)

# Predict
new_text = "Charlie works for Tech Corp"
prediction = clf.predict(vectorizer.transform([new_text]))
print(prediction)  # Output: ['WORKS_AT']
```

**Pros:**
- Learns patterns from examples
- Handles unseen variations
- Adapts to domain

**Cons:**
- Requires labeled training data
- Harder to interpret decisions
- Slower inference

### Technique 4: Transformer-Based Models

Use pre-trained language models for relation extraction:

```python
from transformers import pipeline

# Zero-shot relation extraction
classifier = pipeline("zero-shot-classification", 
                      model="facebook/bart-large-mnli")

text = "Alice works at Acme"
candidate_relations = ["WORKS_AT", "OWNS", "MANAGES", "KNOWS"]

result = classifier(text, candidate_relations, multi_class=True)
print(result)
# Output: top scoring relation
```

**Pros:**
- State-of-the-art accuracy
- Handles complex patterns
- Supports zero-shot learning

**Cons:**
- Computationally expensive
- Requires GPU for speed
- Large model sizes

---

## Handling Ambiguity

### Ambiguous Verbs

**Challenge:**
```
"Alice is at Acme"
- "is at" could mean: WORKS_AT, VISITS, LOCATED_AT?
```

**Resolution:**
```
Use context:
- If Alice is a Person and Acme is a Company → WORKS_AT (contextually likely)
- If event mentions employment → WORKS_AT
- If event mentions temporary visit → VISITS
- Consult schema constraints
```

### Multiple Relationships

**Challenge:**
```
"Alice works at and owns Acme"
- One sentence, two relationships
```

**Solution:**
```
Identify conjunction:
- Relationship 1: Alice -WORKS_AT-> Acme
- Relationship 2: Alice -OWNS-> Acme
- Coordinate both predicates
```

### Implicit Relationships

**Challenge:**
```
"The CEO of Acme, Alice, earned $5M"
- CEO role implies MANAGES relationship
- Implicit: Alice manages Acme employees
```

**Solution:**
```
Use background knowledge:
- "CEO of [Company]" → CEO MANAGES Company
- Infer from role descriptions
```

---

## Advanced Patterns

### Transitive Relations

```
"Alice works at Acme. Acme is in New York."
Inference: Alice (indirectly) LOCATED_IN New York
```

### N-ary Relations

Relations involving more than 2 entities:

```
"Alice works at Acme in the Sales department"

Entities: Alice (Person), Acme (Company), Sales (Department)
Relations:
- Alice WORKS_AT Acme
- Alice WORKS_IN Sales
- Sales PART_OF Acme
```

### Negation

```
"Alice does not work at Acme"
- Negated relationship
- Store as: WORKS_AT with negation flag = true
```

---

## Evaluation

### Standard Metrics

```
Precision = (Correct Relations) / (Predicted Relations)
Recall = (Correct Relations) / (Gold Standard Relations)
F1-Score = 2 * (Precision * Recall) / (Precision + Recall)
```

### Benchmark Datasets

- SemEval 2010 Task 8 (relation classification)
- TACL (temporal and causal relations)
- OntoNotes (coreference and relations)

---

## Best Practices

✓ Validate relationships against schema  
✓ Handle both directions explicitly  
✓ Extract relationship properties when available  
✓ Use contextual clues for disambiguation  
✓ Test on diverse domains  
✓ Log ambiguous cases for review  
✓ Update mappings based on domain feedback  

---

## Common Relationship Patterns

### Employment Domain

```
works_at, works_for, employed_by, manages, reports_to, 
department_of, team_member_of, hired_by
```

### Commerce Domain

```
purchased, sold_to, owns, manufactures, supplies, 
buys_from, delivers_to, invoiced_by
```

### Social Domain

```
knows, friends_with, follows, likes, married_to, 
lives_with, worked_with, studied_with
```

### Geographic Domain

```
located_in, borders, capital_of, region_of, 
near, adjacent_to, connects_to
```

---

## See Also

- [Entity Recognition](entity-recognition.md)
- [Query Patterns Reference](query-patterns.md)
- [Dependency Parsing Tutorial](https://www.coursera.org/specializations/natural-language-processing)

