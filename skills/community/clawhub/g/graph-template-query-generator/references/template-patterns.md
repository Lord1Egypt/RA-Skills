# Query Template Patterns

Twenty+ comprehensive design patterns for query template generation, covering systematic approaches to creating reusable, parameterized graph queries across Cypher and SPARQL.

---

## Node Lookup Patterns (4)

### Pattern 1: Simple Node Lookup by ID

**Context:** Finding a single node by its primary identifier.

**Template:**
```cypher
MATCH (n:$label {id: $id})
RETURN n
```

**Parameters:**
```json
{
  "label": "Person",
  "id": "P12345"
}
```

**When to Use:**
- Single entity retrieval
- ID-based queries
- Primary key lookups

**Performance:** O(1) with index on id

---

### Pattern 2: Node Lookup by Property

**Context:** Finding nodes by a specific property value.

**Template:**
```cypher
MATCH (n:$label {$property: $value})
RETURN n
LIMIT $limit
```

**Parameters:**
```json
{
  "label": "Person",
  "property": "email",
  "value": "alice@example.com",
  "limit": 10
}
```

**Index Recommendation:**
```cypher
CREATE INDEX ON :Person(email)
```

---

### Pattern 3: Multi-Property Node Lookup

**Context:** Finding nodes matching multiple property conditions.

**Template:**
```cypher
MATCH (n:$label {$property1: $value1, $property2: $value2})
RETURN n
```

**Parameters:**
```json
{
  "label": "Person",
  "property1": "firstName",
  "value1": "John",
  "property2": "lastName",
  "value2": "Smith"
}
```

**Index Recommendation:**
```cypher
CREATE INDEX ON :Person(firstName, lastName)
```

---

### Pattern 4: Node Lookup with Filtering

**Context:** Finding nodes and filtering by additional conditions.

**Template:**
```cypher
MATCH (n:$label {$property: $value})
WHERE n.$filterProp $operator $filterValue
RETURN n
LIMIT $limit
```

**Parameters:**
```json
{
  "label": "Person",
  "property": "status",
  "value": "active",
  "filterProp": "age",
  "operator": ">",
  "filterValue": 18,
  "limit": 50
}
```

---

## Relationship Patterns (5)

### Pattern 5: Direct Relationship Traversal

**Context:** Traversing a single relationship type between specific node types.

**Template:**
```cypher
MATCH (a:$sourceLabel)-[:$relationshipType]->(b:$targetLabel)
RETURN a, b
LIMIT $limit
```

**Parameters:**
```json
{
  "sourceLabel": "Person",
  "relationshipType": "WORKS_AT",
  "targetLabel": "Company",
  "limit": 100
}
```

**Usage:** Common relationship queries (employs, follows, owns, etc.)

---

### Pattern 6: Bidirectional Relationship Query

**Context:** Following relationships in either direction.

**Template:**
```cypher
MATCH (a:$label1)-[:$relationshipType]-(b:$label2)
RETURN a, b, type(relationship) as rel_type
LIMIT $limit
```

**Parameters:**
```json
{
  "label1": "Person",
  "label2": "Organization",
  "relationshipType": "ASSOCIATED_WITH",
  "limit": 50
}
```

**Use Cases:** Symmetric relationships (friends, colleagues, partners)

---

### Pattern 7: Relationship with Property Filter

**Context:** Traversing relationships and filtering by relationship properties.

**Template:**
```cypher
MATCH (a:$sourceLabel)-[r:$relationshipType {$property: $value}]->(b:$targetLabel)
RETURN a, b, r.$property
LIMIT $limit
```

**Parameters:**
```json
{
  "sourceLabel": "Person",
  "relationshipType": "EMPLOYED_AT",
  "property": "status",
  "value": "active",
  "targetLabel": "Company",
  "limit": 50
}
```

---

### Pattern 8: Relationship Count

**Context:** Finding nodes and counting their relationships.

**Template:**
```cypher
MATCH (n:$label)-[r:$relationshipType]->()
RETURN n, COUNT(r) as relationship_count
ORDER BY relationship_count DESC
LIMIT $limit
```

**Parameters:**
```json
{
  "label": "Person",
  "relationshipType": "FOLLOWS",
  "limit": 20
}
```

**Use Cases:** Finding influential nodes, popular items, high-degree nodes

---

### Pattern 9: Relationship Aggregation

**Context:** Aggregating data across relationships.

**Template:**
```cypher
MATCH (source:$sourceLabel)-[:$relationshipType]->(target:$targetLabel)
RETURN target.$groupProperty, COUNT(DISTINCT source) as count, AVG(source.$metric) as avg
GROUP BY target.$groupProperty
ORDER BY count DESC
LIMIT $limit
```

**Parameters:**
```json
{
  "sourceLabel": "Order",
  "relationshipType": "PLACED_BY",
  "targetLabel": "Customer",
  "groupProperty": "segment",
  "metric": "amount",
  "limit": 10
}
```

---

## Path Patterns (4)

### Pattern 10: Bounded Path Discovery

**Context:** Finding paths between nodes with maximum depth limit.

**Template:**
```cypher
MATCH path = (start:$startLabel)-[*1..$depth]-(end:$endLabel)
RETURN path, LENGTH(path) as hops
LIMIT $limit
```

**Parameters:**
```json
{
  "startLabel": "Person",
  "endLabel": "Person",
  "depth": 3,
  "limit": 10
}
```

**Best Practice:** Always bind depth to prevent exponential explosion

---

### Pattern 11: Path with Type Constraint

**Context:** Finding paths using only specific relationship types.

**Template:**
```cypher
MATCH path = (start:$startLabel)-[:$relationType*1..$depth]-(end:$endLabel)
RETURN path, nodes(path) as nodes, relationships(path) as relationships
LIMIT $limit
```

**Parameters:**
```json
{
  "startLabel": "Person",
  "relationType": "CONNECTED_TO",
  "endLabel": "Person",
  "depth": 4,
  "limit": 20
}
```

---

### Pattern 12: Shortest Path

**Context:** Finding the shortest path between two nodes.

**Template:**
```cypher
MATCH path = shortestPath((start:$startLabel)-[*]-(end:$endLabel))
RETURN path, LENGTH(path) as distance
LIMIT $limit
```

**Parameters:**
```json
{
  "startLabel": "Person",
  "endLabel": "Person",
  "limit": 1
}
```

**Performance:** O(n) with pruning, use LIMIT 1

---

### Pattern 13: Path with Filter

**Context:** Finding paths and filtering by node or relationship properties.

**Template:**
```cypher
MATCH path = (start:$startLabel)-[*1..$depth]-(end:$endLabel)
WHERE ALL(n in nodes(path) WHERE n.$property = $value)
RETURN path, LENGTH(path) as hops
LIMIT $limit
```

**Parameters:**
```json
{
  "startLabel": "Person",
  "endLabel": "Company",
  "depth": 3,
  "property": "status",
  "value": "active",
  "limit": 10
}
```

---

## Aggregation Patterns (4)

### Pattern 14: Group By Aggregation

**Context:** Grouping results and computing statistics.

**Template:**
```cypher
MATCH (source:$sourceLabel)-[:$relationshipType]->(target:$targetLabel)
RETURN target.$groupBy, COUNT(source) as count, COLLECT(source.id) as ids
GROUP BY target.$groupBy
ORDER BY count DESC
LIMIT $limit
```

**Parameters:**
```json
{
  "sourceLabel": "Transaction",
  "relationshipType": "INITIATED_BY",
  "targetLabel": "User",
  "groupBy": "region",
  "limit": 20
}
```

---

### Pattern 15: Multi-Level Aggregation

**Context:** Aggregating at multiple levels.

**Template:**
```cypher
MATCH (a:$label1)-[:$rel1]->(b:$label2)-[:$rel2]->(c:$label3)
RETURN a.$prop1, b.$prop2, COUNT(c) as count
GROUP BY a.$prop1, b.$prop2
ORDER BY count DESC
LIMIT $limit
```

**Parameters:**
```json
{
  "label1": "Department",
  "rel1": "CONTAINS",
  "label2": "Team",
  "rel2": "LEADS",
  "label3": "Employee",
  "prop1": "name",
  "prop2": "name",
  "limit": 50
}
```

---

### Pattern 16: Aggregation with Having

**Context:** Filtering aggregated groups by conditions.

**Template:**
```cypher
MATCH (source:$sourceLabel)-[:$relationshipType]->(target:$targetLabel)
WITH target.$groupProperty, COUNT(source) as item_count
WHERE item_count > $minCount
RETURN target.$groupProperty, item_count
ORDER BY item_count DESC
LIMIT $limit
```

**Parameters:**
```json
{
  "sourceLabel": "Order",
  "relationshipType": "CONTAINS",
  "targetLabel": "Item",
  "groupProperty": "category",
  "minCount": 10,
  "limit": 20
}
```

---

### Pattern 17: Complex Aggregation with Math

**Context:** Computing statistical measures.

**Template:**
```cypher
MATCH (item:$itemLabel)-[:$relationshipType]-(stat)
RETURN item.$groupBy,
       COUNT(stat) as count,
       AVG(stat.$metric) as average,
       MAX(stat.$metric) as maximum,
       MIN(stat.$metric) as minimum
GROUP BY item.$groupBy
ORDER BY average DESC
LIMIT $limit
```

**Parameters:**
```json
{
  "itemLabel": "Product",
  "relationshipType": "HAS_SALE",
  "metric": "amount",
  "groupBy": "category",
  "limit": 10
}
```

---

## Filtering Patterns (3)

### Pattern 18: Simple WHERE Filter

**Context:** Filtering nodes by property conditions.

**Template:**
```cypher
MATCH (n:$label)
WHERE n.$property $operator $value
RETURN n
LIMIT $limit
```

**Parameters:**
```json
{
  "label": "Person",
  "property": "age",
  "operator": ">",
  "value": 30,
  "limit": 50
}
```

---

### Pattern 19: Complex WHERE with AND/OR

**Context:** Multi-condition filtering.

**Template:**
```cypher
MATCH (n:$label)
WHERE (n.$prop1 $op1 $val1 AND n.$prop2 $op2 $val2)
   OR (n.$prop3 $op3 $val3)
RETURN n
LIMIT $limit
```

**Parameters:**
```json
{
  "label": "Product",
  "prop1": "price",
  "op1": ">",
  "val1": 100,
  "prop2": "in_stock",
  "op2": "=",
  "val2": true,
  "prop3": "category",
  "op3": "=",
  "val3": "Featured",
  "limit": 100
}
```

---

### Pattern 20: String Pattern Matching

**Context:** Finding nodes by text patterns.

**Template:**
```cypher
MATCH (n:$label)
WHERE n.$property CONTAINS $searchTerm
   OR n.$property STARTS WITH $prefix
RETURN n
LIMIT $limit
```

**Parameters:**
```json
{
  "label": "Document",
  "property": "title",
  "searchTerm": "graph",
  "prefix": "Database",
  "limit": 25
}
```

---

## SPARQL Specific Patterns (2)

### Pattern 21: SPARQL Optional Pattern

**Context:** Finding entities with optional properties.

**Template:**
```sparql
PREFIX ex: <http://example.org/>

SELECT ?entity ?name ?email
WHERE {
  ?entity a ex:$class .
  ?entity ex:name ?name .
  OPTIONAL { ?entity ex:email ?email }
}
LIMIT $limit
```

**Parameters:**
```json
{
  "class": "Person",
  "limit": 50
}
```

---

### Pattern 22: SPARQL Filter with Multiple Conditions

**Context:** Filtering SPARQL results by multiple criteria.

**Template:**
```sparql
PREFIX ex: <http://example.org/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?entity ?value
WHERE {
  ?entity a ex:$class ;
          ex:$property ?value .
  FILTER (?value > $minValue && ?value < $maxValue)
  FILTER (LANG(?label) = $lang)
}
LIMIT $limit
```

**Parameters:**
```json
{
  "class": "Item",
  "property": "price",
  "minValue": 100,
  "maxValue": 1000,
  "lang": "en",
  "limit": 50
}
```

---

## Advanced Patterns (4)

### Pattern 23: Template Composition

**Context:** Combining multiple templates.

**Usage:**
```python
# Base template
base = generator.get_template("find_nodes")
# Add filter
filter_template = generator.get_template("add_filter")
# Combine
combined = compose_templates(base, filter_template)
```

---

### Pattern 24: Parameterized Limit

**Context:** Dynamic result limiting.

**Template:**
```cypher
MATCH (n:$label)
RETURN n
LIMIT CASE
  WHEN $resultSize = 'small' THEN 10
  WHEN $resultSize = 'medium' THEN 50
  WHEN $resultSize = 'large' THEN 500
  ELSE 100
END
```

---

### Pattern 25: Template with Default Parameters

**Context:** Templates with sensible defaults.

**Template:**
```python
template = {
  "query": "MATCH (n:$label) RETURN n LIMIT $limit",
  "parameters": {
    "label": None,  # Required
    "limit": 10     # Default: 10
  }
}
```

---

## Template Best Practices Summary

### 1. Naming Conventions
✅ Use `$parameterName` format  
✅ Use clear, descriptive names  
✅ Avoid single letters  
✅ Use snake_case for multi-word parameters

### 2. Performance Optimization
✅ Always include LIMIT clause  
✅ Index queried properties  
✅ Bound path depth (max 3-4)  
✅ Avoid SELECT * patterns

### 3. Reusability
✅ Parameterize all variable values  
✅ Make templates language-agnostic where possible  
✅ Document expected parameter types  
✅ Provide default behaviors

### 4. Maintainability
✅ Include clear comments  
✅ Version templates  
✅ Document schema assumptions  
✅ Provide update procedures

### 5. Documentation
✅ Purpose statement  
✅ Parameter descriptions  
✅ Usage examples  
✅ Performance characteristics  
✅ Index recommendations

---

## Template Quality Checklist

For each template, verify:

- [ ] All dynamic values are parameterized
- [ ] Query is syntactically valid
- [ ] Appropriate indexes are recommended
- [ ] LIMIT clause prevents runaway results
- [ ] Parameters have clear names
- [ ] Parameter types are documented
- [ ] Usage example is provided
- [ ] Performance characteristics noted
- [ ] Works across different data sizes
- [ ] Error cases are handled

---

**Status: Production-Ready Template Patterns**

These 25+ patterns provide comprehensive guidance for systematic template generation across Cypher, SPARQL, and other graph query languages.

