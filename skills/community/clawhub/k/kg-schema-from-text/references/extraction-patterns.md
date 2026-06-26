# Entity & Relationship Extraction Patterns

This guide provides patterns for extracting schema elements from natural language text.

## Entity Extraction

### Pattern Recognition

**Nouns & Noun Phrases** = Potential entities

Common indicators:
- Capitalized words: `Student`, `Professor`
- Compound nouns: `Department Head`, `Course Catalog`
- Acronyms: `KG` (Knowledge Graph), `RDF` (Resource Description Framework)

**Examples:**

| Text | Entities |
|------|----------|
| "Students enroll in courses" | Student, Course |
| "A library has books and members" | Library, Book, Member |
| "Employees work in departments" | Employee, Department |

### Extraction Algorithm

```
1. Extract all nouns from text
2. Group related nouns (synonyms, compound nouns)
3. Normalize naming (singular, PascalCase)
4. Remove generic nouns (thing, item, data)
5. Return entity list
```

---

## Relationship Extraction

### Pattern Recognition

**Verbs & Prepositions** = Potential relationships

Common patterns:
- Active verbs: `enrolls in`, `teaches`, `manages`
- Prepositions: `located in`, `belongs to`, `has`
- Compound: `is managed by`, `is part of`

**Examples:**

| Text | Relationships |
|------|---------------|
| "Students enroll in courses" | Student -[ENROLLED_IN]-> Course |
| "Professors teach courses" | Professor -[TEACHES]-> Course |
| "Departments manage professors" | Department -[MANAGES]-> Professor |

### Extraction Algorithm

```
1. Extract verb phrases and prepositions
2. Identify subject and object entities
3. Normalize relationship naming (SCREAMING_SNAKE_CASE)
4. Determine direction (subject -> object)
5. Remove redundant relationships
6. Return relationship list
```

---

## Property Extraction

### Identifying Properties

Look for **descriptive attributes** mentioned for entities:

**Patterns:**
- "Student has name, email, enrollment date"
- "Course includes title, credits, description"
- "Department contains budget, location"

**By Context:**

| Entity Type | Common Properties |
|-------------|------------------|
| Person | name, email, phone, address, id |
| Document | title, date, author, content, status |
| Location | name, address, coordinates, population |
| Organization | name, founded_date, headquarters, industry |

### Extraction Guidelines

1. Attributes mentioned after entity definition
2. Properties from examples or sample data
3. Derived from relationship context
4. Domain-specific attributes
5. Standard identifiers (id, UUID)

---

## Normalization Rules

### Entity Naming

✓ **DO:**
- Use singular nouns: `Student` not `Students`
- Use PascalCase: `StudentCourse` not `student_course`
- Be descriptive: `Enrollment` not `E`

✗ **DON'T:**
- Use abbreviations: `Stud`, `Prof`
- Mix case styles: `Student_course`
- Use generic names: `Item`, `Data`

### Relationship Naming

✓ **DO:**
- Use verbs: `ENROLLED_IN`, `TEACHES`, `MANAGES`
- Use SCREAMING_SNAKE_CASE: `ENROLLED_IN`
- Be specific: `TEACHES` not `RELATES`

✗ **DON'T:**
- Use abbreviations: `E_I` for `ENROLLED_IN`
- Use lowercase: `enrolled_in`
- Be vague: `HAS`, `IS`

### Property Naming

✓ **DO:**
- Use snake_case: `first_name`, `enrollment_date`
- Match domain vocabulary
- Include data type hints

✗ **DON'T:**
- Use spaces: `first name`
- Mix styles: `firstName_last_name`
- Use abbreviations: `nm` for `name`

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Ambiguous relationships | Clarify direction, context |
| Duplicate entities (Student vs Learner) | Consolidate synonyms |
| Missing properties | Check domain requirements |
| Circular relationships | Review necessity, document cycles |
| Over-generalization | Split into more specific entities |

---

## Examples

### University Domain

**Text:**
```
A university has departments. Each department has professors and courses.
Professors teach courses. Students enroll in courses.
Each course has prerequisites.
```

**Extracted Schema:**
```
Entities:
- University
- Department
- Professor
- Course
- Student

Relationships:
- University -[HAS]-> Department
- Department -[HAS]-> Professor
- Department -[HAS]-> Course
- Professor -[TEACHES]-> Course
- Course -[REQUIRES]-> Course (prerequisite)
- Student -[ENROLLED_IN]-> Course

Properties:
- University: name, city, founded_year
- Department: name, budget, chair
- Professor: name, email, specialization
- Course: code, title, credits, description
- Student: id, name, email
```

### E-Commerce Domain

**Text:**
```
Customers place orders. Each order contains products.
Products belong to categories. Suppliers provide products.
```

**Extracted Schema:**
```
Entities:
- Customer
- Order
- Product
- Category
- Supplier

Relationships:
- Customer -[PLACES]-> Order
- Order -[CONTAINS]-> Product
- Product -[BELONGS_TO]-> Category
- Supplier -[PROVIDES]-> Product

Properties:
- Customer: id, name, email, phone
- Order: id, date, total_amount, status
- Product: id, name, price, sku, description
- Category: id, name, description
- Supplier: id, name, contact, rating
```

---

See [example-schemas.md](../examples/example-schemas.md) for more domain examples.

