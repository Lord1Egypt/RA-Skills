# Class & ER Diagram Syntax

## Class Diagram

### Basic Structure

```mermaid
classDiagram
  class User {
    +String name
    +String email
    -String passwordHash
    +login() bool
    +logout()
  }

  class Order {
    +int id
    +Date createdAt
    +float total
    +place()
    +cancel()
  }

  User "1" --> "*" Order : places
```

### Visibility Modifiers

| Symbol | Meaning |
|--------|---------|
| `+` | Public |
| `-` | Private |
| `#` | Protected |
| `~` | Package/Internal |

### Relationships

| Syntax | Type | Meaning |
|--------|------|---------|
| `<\|--` | Inheritance | extends |
| `*--` | Composition | owns (lifecycle) |
| `o--` | Aggregation | has (independent) |
| `-->` | Association | uses |
| `..>` | Dependency | depends on |
| `..\|>` | Realization | implements |

### Cardinality

```mermaid
classDiagram
  User "1" --> "*" Order : places
  Order "1" --> "1..*" OrderItem : contains
  Product "0..*" --> "0..*" Category : belongs to
```

| Notation | Meaning |
|----------|---------|
| `1` | Exactly one |
| `0..1` | Zero or one |
| `*` | Many |
| `1..*` | One or more |
| `n..m` | Range |

### Abstract Classes & Interfaces

```mermaid
classDiagram
  class Shape {
    <<abstract>>
    +area()* float
  }

  class Drawable {
    <<interface>>
    +draw()
  }

  Shape <|-- Circle
  Drawable <|.. Circle
```

- `<<abstract>>` / `<<interface>>` — stereotype annotation on its own line inside the class.
- A trailing `*` on a method marks it abstract: `+area()* float`.

### Class Best Practices

- Show only the attributes / methods relevant to the diagram's point.
- Use inheritance sparingly; prefer composition for reuse.
- Indicate cardinality on associations; group related classes together.

---

## ER Diagram

### Basic Structure

```mermaid
erDiagram
  USER ||--o{ ORDER : places
  ORDER ||--|{ ORDER_ITEM : contains
  PRODUCT ||--o{ ORDER_ITEM : "included in"

  USER {
    int id PK
    string name
    string email
    datetime created_at
  }

  ORDER {
    int id PK
    int user_id FK
    float total
    string status
  }

  ORDER_ITEM {
    int order_id FK
    int product_id FK
    int quantity
  }
```

### Relationship Notation

| Left | Right | Meaning |
|------|-------|---------|
| `\|\|` | `\|\|` | One to one |
| `\|\|` | `o{` | One to zero or many |
| `\|\|` | `\|{` | One to one or many |
| `o\|` | `o{` | Zero or one to zero or many |
| `}o` | `o{` | Zero or many to zero or many |
| `}\|` | `\|{` | One or many to one or many |

The relation reads `LEFT REL--REL RIGHT`, e.g. `CUSTOMER ||--o{ ORDER`.

### Attribute Types

```mermaid
erDiagram
  PRODUCT {
    int id PK "Primary key"
    string name "Product name"
    float price
    int category_id FK "Foreign key"
    string sku UK "Unique key"
  }
```

Markers: `PK` (primary), `FK` (foreign), `UK` (unique). Use standard SQL-ish types (`int`, `string`, `decimal`, `date`, `bool`).

### ER Best Practices

- UPPERCASE entity names, snake_case attribute names.
- Always mark `PK` and `FK`; show only essential attributes.
- Keep relationship labels short; limit to ~6–8 entities per diagram.
