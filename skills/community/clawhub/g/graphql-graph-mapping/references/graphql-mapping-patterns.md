# GraphQL Graph Mapping - Design Patterns

Comprehensive patterns for mapping GraphQL schemas and queries to graph database operations.

---

## 1. Type Mapping Patterns

### 1.1 Object Type to Node Label Pattern

**Pattern:** GraphQL object types map directly to graph node labels.

```graphql
type Person {
  id: ID!
  name: String!
  age: Int
}
```

**Mapping:**
```
GraphQL Type: Person
→ Graph Label: :Person
→ Node Properties: {id, name, age}
```

**Usage:**
- Basic entity representation
- Each GraphQL type has one primary label
- Properties are node properties

**Best Practice:**
Use consistent naming between GraphQL and graph database.

---

### 1.2 Scalar Field to Property Pattern

**Pattern:** GraphQL scalar fields map to node properties.

```graphql
type Product {
  id: ID!
  name: String!
  price: Float!
  inStock: Boolean!
  createdAt: String!
}
```

**Mapping:**
```
name: String! → Product.name (String property)
price: Float! → Product.price (Float property)
inStock: Boolean! → Product.inStock (Boolean property)
createdAt: String! → Product.createdAt (DateTime property)
```

**Cypher:**
```cypher
MATCH (p:Product {id: $id})
RETURN p.name, p.price, p.inStock, p.createdAt
```

---

### 1.3 Relationship Field to Edge Pattern

**Pattern:** GraphQL fields returning object types map to relationship traversals.

```graphql
type Person {
  id: ID!
  name: String!
  knows: [Person!]!
  worksAt: Company!
}

type Company {
  id: ID!
  name: String!
}
```

**Mapping:**
```
knows: [Person!]! → (Person)-[:KNOWS]->(Person) relationship
worksAt: Company! → (Person)-[:WORKS_AT]->(Company) relationship
```

**Cypher:**
```cypher
MATCH (p:Person {id: $id})
RETURN p.name,
       [(p)-[:KNOWS]->(friend:Person) | {id: friend.id, name: friend.name}] AS knows,
       [(p)-[:WORKS_AT]->(company:Company) | {id: company.id, name: company.name}] AS worksAt
```

---

### 1.4 Interface Implementation Pattern

**Pattern:** GraphQL interfaces map to multiple node labels.

```graphql
interface Entity {
  id: ID!
  name: String!
}

type Person implements Entity {
  id: ID!
  name: String!
  email: String!
}

type Company implements Entity {
  id: ID!
  name: String!
  industry: String!
}
```

**Mapping:**
```
GraphQL Interface → Base properties (id, name)
GraphQL Implementation → Additional properties
```

**Cypher - Polymorphic Query:**
```cypher
MATCH (e:Person|Company {id: $id})
RETURN e.id, e.name,
       CASE labels(e)[0] 
         WHEN 'Person' THEN {email: e.email}
         WHEN 'Company' THEN {industry: e.industry}
       END AS additionalProperties
```

---

## 2. Query Translation Patterns

### 2.1 Root Query to Node Match Pattern

**Pattern:** Root GraphQL query fields translate to node matching.

```graphql
type Query {
  user(id: ID!): User
  userByEmail(email: String!): User
}
```

**GraphQL Query:**
```graphql
{
  user(id: "usr_123") {
    name
  }
}
```

**Cypher Translation:**
```cypher
MATCH (u:User {id: $id})
RETURN u.name
```

**Gremlin Translation:**
```gremlin
g.V().has("User", "id", "usr_123")
  .values("name")
```

---

### 2.2 Nested Field Selection Pattern

**Pattern:** Nested GraphQL fields translate to result projections.

```graphql
{
  user(id: "usr_123") {
    name
    email
    age
  }
}
```

**Cypher - Property Selection:**
```cypher
MATCH (u:User {id: "usr_123"})
RETURN u.name, u.email, u.age
```

**Optimization:** Only select required fields.

---

### 2.3 Nested Relationship Traversal Pattern

**Pattern:** Nested object fields translate to relationship traversals.

```graphql
{
  user(id: "usr_123") {
    name
    company {
      name
      industry
    }
  }
}
```

**Cypher Translation:**
```cypher
MATCH (u:User {id: "usr_123"})-[:WORKS_AT]->(c:Company)
RETURN u.name, c.name, c.industry
```

**Multi-level Traversal:**
```graphql
{
  user(id: "usr_123") {
    name
    company {
      name
      employees {
        name
      }
    }
  }
}
```

**Cypher:**
```cypher
MATCH (u:User {id: "usr_123"})
       -[:WORKS_AT]->(c:Company)
       <-[:WORKS_AT]-(e:User)
RETURN u.name, c.name, collect(e.name) AS employees
```

---

### 2.4 Filtered Query Pattern

**Pattern:** GraphQL arguments translate to WHERE clauses and filters.

```graphql
{
  users(where: {age: {gt: 30}}) {
    name
    age
  }
}
```

**Cypher Translation:**
```cypher
MATCH (u:User)
WHERE u.age > 30
RETURN u.name, u.age
```

**Complex Filters:**
```graphql
{
  users(where: {
    AND: [
      {age: {gt: 30}}
      {company: {industry: "Technology"}}
    ]
  }) {
    name
  }
}
```

**Cypher:**
```cypher
MATCH (u:User)-[:WORKS_AT]->(c:Company)
WHERE u.age > 30 AND c.industry = "Technology"
RETURN u.name
```

---

### 2.5 Pagination Pattern

**Pattern:** GraphQL pagination arguments translate to LIMIT and OFFSET.

```graphql
{
  users(first: 10, after: "cursor_abc") {
    nodes {
      name
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

**Cypher Translation:**
```cypher
MATCH (u:User)
WITH u SKIP $skip LIMIT $limit
COLLECT(u) AS users
RETURN users, 
       size(users) < $limit AS hasNextPage,
       users[-1].id AS endCursor
```

---

### 2.6 Aggregation Pattern

**Pattern:** GraphQL aggregation fields translate to count/sum/avg operations.

```graphql
{
  userStats {
    totalCount
    averageAge
    byCompany {
      company {
        name
      }
      count
    }
  }
}
```

**Cypher Translation:**
```cypher
MATCH (u:User)
RETURN count(u) AS totalCount,
       avg(u.age) AS averageAge,
       [(u)-[:WORKS_AT]->(c:Company) | {company: {name: c.name}, count: count(u)}] AS byCompany
```

---

## 3. Filter and Argument Patterns

### 3.1 Comparison Operators Pattern

**Pattern:** GraphQL comparison operators map to Cypher/SQL operators.

```graphql
where: {
  age: {eq: 30}           # equals
  age: {ne: 30}           # not equals
  age: {gt: 30}           # greater than
  age: {gte: 30}          # greater than or equal
  age: {lt: 30}           # less than
  age: {lte: 30}          # less than or equal
  age: {in: [25, 30, 35]} # in list
}
```

**Cypher Mapping:**
```cypher
u.age = 30              # eq
u.age <> 30             # ne
u.age > 30              # gt
u.age >= 30             # gte
u.age < 30              # lt
u.age <= 30             # lte
u.age IN [25, 30, 35]   # in
```

---

### 3.2 String Filters Pattern

**Pattern:** String-specific filters for pattern matching.

```graphql
where: {
  name: {contains: "John"}        # substring
  name: {startsWith: "J"}         # prefix
  name: {endsWith: "n"}           # suffix
  email: {matches: ".*@company.*"}# regex
}
```

**Cypher Mapping:**
```cypher
u.name CONTAINS "John"                    # contains
u.name STARTS WITH "J"                    # startsWith
u.name ENDS WITH "n"                      # endsWith
u.email =~ ".*@company.*"                 # matches (regex)
```

---

### 3.3 Boolean Logic Pattern

**Pattern:** Combine filters with AND, OR, NOT logic.

```graphql
where: {
  AND: [
    {age: {gt: 30}}
    {company: {industry: "Tech"}}
  ]
}

where: {
  OR: [
    {status: "Active"}
    {status: "Pending"}
  ]
}

where: {NOT: {status: "Inactive"}}
```

**Cypher Mapping:**
```cypher
WHERE u.age > 30 AND c.industry = "Tech"

WHERE u.status = "Active" OR u.status = "Pending"

WHERE NOT u.status = "Inactive"
```

---

## 4. Result Mapping Patterns

### 4.1 Single Object Pattern

**Pattern:** Single node result maps to GraphQL object.

**Graph Result:**
```json
{
  "id": "usr_123",
  "name": "Alice",
  "age": 30
}
```

**GraphQL Response:**
```json
{
  "data": {
    "user": {
      "id": "usr_123",
      "name": "Alice",
      "age": 30
    }
  }
}
```

---

### 4.2 List/Collection Pattern

**Pattern:** Multiple nodes map to GraphQL list.

**Graph Results:**
```json
[
  {"id": "usr_1", "name": "Alice"},
  {"id": "usr_2", "name": "Bob"}
]
```

**GraphQL Response:**
```json
{
  "data": {
    "users": [
      {"id": "usr_1", "name": "Alice"},
      {"id": "usr_2", "name": "Bob"}
    ]
  }
}
```

---

### 4.3 Nested Object Pattern

**Pattern:** Relationship results map to nested GraphQL objects.

**Graph Result (Cypher):**
```
(User {name: "Alice"})-[:WORKS_AT]->(Company {name: "TechCorp"})
```

**GraphQL Response:**
```json
{
  "data": {
    "user": {
      "name": "Alice",
      "company": {
        "name": "TechCorp"
      }
    }
  }
}
```

---

### 4.4 Null Handling Pattern

**Pattern:** Missing relationships or optional fields map to null.

**GraphQL Query:**
```graphql
{
  user(id: "usr_123") {
    name
    manager {          # May be null if no manager
      name
    }
  }
}
```

**Cypher:**
```cypher
MATCH (u:User {id: "usr_123"})
OPTIONAL MATCH (u)-[:REPORTS_TO]->(m:User)
RETURN u.name, m.name
```

**GraphQL Response:**
```json
{
  "data": {
    "user": {
      "name": "Alice",
      "manager": null
    }
  }
}
```

---

### 4.5 Alias Resolution Pattern

**Pattern:** GraphQL aliases map to renamed fields in response.

**GraphQL Query:**
```graphql
{
  currentCompany: company(id: "comp_1") {
    name
  }
  previousCompany: company(id: "comp_2") {
    name
  }
}
```

**GraphQL Response:**
```json
{
  "data": {
    "currentCompany": {"name": "TechCorp"},
    "previousCompany": {"name": "StartupX"}
  }
}
```

---

## 5. Database-Specific Patterns

### 5.1 Neo4j Cypher Collection Pattern

**Pattern:** Neo4j uses collection functions for list fields.

```cypher
MATCH (u:User {id: "usr_123"})
RETURN u.name,
       [(u)-[:KNOWS]->(f:User) | {id: f.id, name: f.name}] AS friends,
       size((u)-[:KNOWS]->()) AS friendCount
```

---

### 5.2 Gremlin Traversal Pattern

**Pattern:** Gremlin uses traversal steps for relationship navigation.

```gremlin
g.V().has("User", "id", "usr_123")
  .project("name", "friends", "friendCount")
  .by("name")
  .by(out("KNOWS").has("User").project("id", "name")
    .by("id")
    .by("name")
    .fold())
  .by(out("KNOWS").count())
```

---

### 5.3 SPARQL Query Pattern

**Pattern:** SPARQL uses triple patterns for RDF graphs.

```sparql
PREFIX ex: <http://example.org/>

SELECT ?name ?friendName
WHERE {
  ex:usr_123 ex:name ?name ;
             ex:knows ?friend .
  ?friend ex:name ?friendName .
}
```

---

## 6. Performance Patterns

### 6.1 Query Depth Limiting Pattern

**Pattern:** Limit nesting depth to prevent expensive queries.

```graphql
# This query depth = 3
{
  user(id: "usr_123") {           # Depth 1
    company {                      # Depth 2
      employees {                  # Depth 3
        projects { ... }           # Would be Depth 4 - DENIED
      }
    }
  }
}
```

**Implementation:**
```python
MAX_QUERY_DEPTH = 3

def validate_query_depth(query_ast):
    if calculate_depth(query_ast) > MAX_QUERY_DEPTH:
        raise QueryDepthExceededError()
```

---

### 6.2 Query Complexity Scoring Pattern

**Pattern:** Score queries by complexity to prevent abuse.

```
Simple field selection: 1 point each
Relationship traversal: 2 points each
List field: multiplied by max items (first: N)
Total max allowed: 1000 points
```

**Example:**
```graphql
{
  user(id: "usr_123") {          # 1 point
    name                          # 1 point
    friends(first: 10) {          # 2 points × 10 items = 20 points
      name                        # 1 point
    }
    company {                     # 2 points
      employees(first: 100) {    # 2 points × 100 items = 200 points
        name                      # 1 point
      }
    }
  }
}
# Total: 228 points (acceptable)
```

---

### 6.3 Field Batching Pattern

**Pattern:** Batch multiple queries to reduce database round-trips.

**Without Batching (N+1 problem):**
```
1. Query user → 1 call
2. Query each user's company → N calls
Total: N+1 calls
```

**With Batching:**
```cypher
MATCH (u:User)
WITH u
MATCH (u)-[:WORKS_AT]->(c:Company)
RETURN u, c
# Single query
```

---

### 6.4 Result Caching Pattern

**Pattern:** Cache frequent query patterns.

```python
@cache(ttl=300)  # 5 minute cache
def get_user_with_friends(user_id):
    return execute_query(user_id)
```

---

## 7. Error Handling Patterns

### 7.1 Missing Field Pattern

**Error:** GraphQL field doesn't exist in graph schema.

```graphql
{
  user(id: "usr_123") {
    nonExistentField  # ERROR: Field not found
  }
}
```

**Handling:**
```json
{
  "errors": [{
    "message": "Cannot query field 'nonExistentField' on type 'User'"
  }]
}
```

---

### 7.2 Invalid Argument Pattern

**Error:** Query argument type mismatch.

```graphql
{
  user(id: 123)  # ERROR: Expected String, got Int
}
```

**Handling:**
```json
{
  "errors": [{
    "message": "Argument 'id' expected type String!, got Int"
  }]
}
```

---

### 7.3 Query Timeout Pattern

**Error:** Query takes too long.

**Handling:**
```python
try:
    result = execute_query(query, timeout=5000)
except QueryTimeoutError:
    return {"errors": [{"message": "Query exceeded timeout"}]}
```

---

## 8. Schema Mapping Patterns

### 8.1 Explicit Schema Mapping Pattern

**Pattern:** Define explicit mapping between GraphQL and graph schemas.

```yaml
graphql_schema:
  User:
    graphLabel: "User"
    properties:
      id:
        graphProperty: "id"
        type: "String"
      name:
        graphProperty: "name"
        type: "String"
    relationships:
      knows:
        graphRelationship: "KNOWS"
        targetType: "User"
```

---

### 8.2 Convention-Based Mapping Pattern

**Pattern:** Use naming conventions for automatic mapping.

**Convention:**
- GraphQL `User` type → Graph `:User` label
- GraphQL `name` field → Graph `name` property
- GraphQL `knows` field → Graph `KNOWS` relationship (uppercase)

---

## 9. Mutation Patterns

### 9.1 Create Node Mutation Pattern

**Pattern:** Mutation creates new graph node.

```graphql
mutation {
  createUser(input: {name: "Alice", age: 30}) {
    id
    name
  }
}
```

**Cypher:**
```cypher
CREATE (u:User {id: $id, name: $name, age: $age})
RETURN u.id, u.name
```

---

### 9.2 Update Node Mutation Pattern

**Pattern:** Mutation updates existing node properties.

```graphql
mutation {
  updateUser(id: "usr_123", input: {age: 31}) {
    id
    name
    age
  }
}
```

**Cypher:**
```cypher
MATCH (u:User {id: "usr_123"})
SET u.age = 31
RETURN u.id, u.name, u.age
```

---

### 9.3 Create Relationship Mutation Pattern

**Pattern:** Mutation creates relationship between nodes.

```graphql
mutation {
  addFriend(userId: "usr_1", friendId: "usr_2") {
    success
  }
}
```

**Cypher:**
```cypher
MATCH (u1:User {id: "usr_1"})
MATCH (u2:User {id: "usr_2"})
CREATE (u1)-[:KNOWS]->(u2)
RETURN true AS success
```

---


