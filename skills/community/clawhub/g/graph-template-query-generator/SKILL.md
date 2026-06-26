---
name: graph-template-query-generator
description: Generate reusable Cypher or SPARQL query templates for common graph database operations such as finding nodes, relationships, paths, and aggregations.
metadata:
  {"openclaw":{"emoji":"📄","homepage":"https://clawhub.com"}}
---

# Template Query Generator

Generate reusable graph query templates for common graph database operations.

This skill produces parameterized query templates that developers can quickly adapt to query graph databases without writing queries from scratch.

It supports template generation for common tasks such as:

- node lookup
- relationship traversal
- path discovery
- aggregations
- filtering
- graph exploration

Templates can be generated for graph query languages such as Cypher and SPARQL.

---

## 📋 Quick Start

### When To Use This Skill

Use this skill when a user wants to:

- generate common graph queries
- create reusable query templates
- quickly scaffold Cypher or SPARQL queries
- explore graph data structures
- build starter queries for applications
- standardize query patterns
- document query patterns

### Example Requests

- "Generate a query template for finding relationships."
- "Create a Cypher template to search nodes by property."
- "Generate a SPARQL query template for retrieving entities."
- "Create a reusable graph query."
- "Give me a template for path discovery."
- "Generate aggregation templates."

---

## 🎯 What This Skill Produces

The skill generates parameterized templates for:

- **Node Queries** - Finding nodes by label and properties
- **Relationship Queries** - Traversing relationships between nodes
- **Path Queries** - Discovering paths through the graph
- **Aggregation Queries** - Computing statistics and summaries
- **Filtering Queries** - Filtering nodes by conditions
- **Graph Exploration** - Discovering graph structure
- **Multi-Hop Queries** - Complex traversals across multiple hops
- **Comparison Queries** - Comparing entities and relationships

Templates typically include **query parameters** to allow easy reuse.

---

## 🔍 Template Categories

### 1. Node Lookup Templates (Basic)

**Cypher template:**
```cypher
MATCH (n:$label {$property: $value})
RETURN n
LIMIT $limit
```

**Example:**
```cypher
MATCH (p:Person {email: $email})
RETURN p
```

**Parameters:**
- `label`: Node label (e.g., Person, Company)
- `property`: Property name (e.g., email, id)
- `value`: Property value
- `limit`: Result limit (default: 10)

---

### 2. Relationship Traversal Templates

**Cypher template:**
```cypher
MATCH (a:$sourceLabel)-[:$relationshipType]->(b:$targetLabel)
RETURN a, b
LIMIT $limit
```

**Example:**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN p, c
```

**Parameters:**
- `sourceLabel`: Starting node label
- `relationshipType`: Relationship type
- `targetLabel`: Target node label
- `limit`: Result limit

---

### 3. Multi-Hop Path Templates

**Cypher template:**
```cypher
MATCH path = (start:$startLabel)-[*1..$depth]-(end:$endLabel)
RETURN path
LIMIT $limit
```

**Example:**
```cypher
MATCH path = (p:Person)-[*1..3]-(target)
RETURN path
LIMIT 50
```

**Parameters:**
- `startLabel`: Starting node label
- `endLabel`: Ending node label
- `depth`: Maximum traversal depth
- `limit`: Result limit

---

### 4. Aggregation Templates

**Cypher template:**
```cypher
MATCH (source:$sourceLabel)-[:$relationshipType]->(target:$targetLabel)
RETURN target.$property, COUNT(DISTINCT source) as count
GROUP BY target.$property
ORDER BY count DESC
LIMIT $limit
```

**Example:**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN c.name, COUNT(DISTINCT p) as employee_count
GROUP BY c.name
ORDER BY employee_count DESC
LIMIT 10
```

---

### 5. Filtering Templates

**Cypher template:**
```cypher
MATCH (n:$label)
WHERE n.$property $operator $value
RETURN n
LIMIT $limit
```

**Example:**
```cypher
MATCH (p:Person)
WHERE p.age > 30
RETURN p
LIMIT 100
```

**Parameters:**
- `label`: Node label
- `property`: Property to filter
- `operator`: Comparison operator (>, <, =, !=)
- `value`: Filter value
- `limit`: Result limit

---

### 6. Property Filtering Templates

**Cypher template:**
```cypher
MATCH (n:$label)
WHERE n.$property CONTAINS $value
RETURN n
LIMIT $limit
```

**Example:**
```cypher
MATCH (p:Product)
WHERE p.description CONTAINS $search_term
RETURN p
LIMIT 20
```

---

### 7. Conditional Aggregation Templates

**Cypher template:**
```cypher
MATCH (source:$sourceLabel)-[:$relationshipType]->(target:$targetLabel)
WHERE target.$filterProperty $operator $filterValue
RETURN target.$groupProperty, COUNT(source) as count
GROUP BY target.$groupProperty
ORDER BY count DESC
LIMIT $limit
```

---

### 8. Relationship Count Templates

**Cypher template:**
```cypher
MATCH (n:$label)-[r:$relationshipType]->()
RETURN n, COUNT(r) as relationship_count
ORDER BY relationship_count DESC
LIMIT $limit
```

**Example:**
```cypher
MATCH (p:Person)-[r:FOLLOWS]->()
RETURN p, COUNT(r) as follower_count
ORDER BY follower_count DESC
LIMIT 10
```

---

## 🔗 SPARQL Template Examples

### SPARQL Node Lookup

```sparql
PREFIX ex: <http://example.org/>
SELECT ?entity
WHERE {
  ?entity a ex:$class ;
          ex:$property $value .
}
LIMIT $limit
```

### SPARQL Relationship Query

```sparql
PREFIX ex: <http://example.org/>
SELECT ?subject ?object
WHERE {
  ?subject ex:$predicate ?object .
}
LIMIT $limit
```

### SPARQL Triple Pattern

```sparql
PREFIX ex: <http://example.org/>
SELECT ?resource
WHERE {
  ?resource a ex:$class .
  ?resource ex:$property ?value .
}
LIMIT $limit
```

---

## 💡 Template Generation Workflow

When generating query templates:

### Step 1: Identify Query Goal
- Node lookup
- Relationship discovery
- Path exploration
- Aggregation
- Filtering

### Step 2: Select Graph Pattern
- Choose appropriate pattern for goal
- Determine node labels/relationship types
- Identify parameterization points

### Step 3: Insert Parameters
- Mark values as `$parameter`
- Choose meaningful parameter names
- Document parameter types

### Step 4: Generate Target Syntax
- Cypher or SPARQL
- Validate syntax
- Include query explanation

### Step 5: Create Usage Example
- Show concrete instantiation
- Document parameter values
- Provide integration guidance

---

## 📋 Output Formats

The skill returns:

### 1. Query Template
Parameterized Cypher or SPARQL query ready for reuse.

### 2. Parameter List
```json
{
  "label": "string - Node label",
  "property": "string - Property name",
  "value": "any - Property value",
  "limit": "integer - Result limit (default: 10)"
}
```

### 3. Query Explanation
Plain English description of query purpose and behavior.

### 4. Usage Example
Concrete instantiation with sample parameter values.

### 5. Performance Notes
Index recommendations and optimization suggestions.

---

## 📈 Template Performance Guidelines

### Node Lookup Templates
- **Performance:** O(1) with index on label + property
- **Index Recommendation:** Create index on queried property
- **Typical Execution:** < 10 ms
- **Best For:** Single entity retrieval

### Relationship Templates
- **Performance:** O(n) where n = source cardinality
- **Index Recommendation:** Index relationship type
- **Typical Execution:** 10-100 ms
- **Best For:** Specific relationship queries

### Path Templates
- **Performance:** O(n^depth) exponential in depth
- **Index Recommendation:** Bound depth to ≤ 3
- **Typical Execution:** 100-1000 ms
- **Best For:** Discovery with bounded depth

### Aggregation Templates
- **Performance:** O(n log n) with grouping
- **Index Recommendation:** Index group property
- **Typical Execution:** 50-500 ms
- **Best For:** Statistical summaries

---

## ✅ Best Practices

When designing query templates:

1. **Use Clear Parameter Names**
   - `$email` instead of `$e`
   - `$depth` instead of `$d`
   - `$company_name` instead of `$c_n`

2. **Include Result Limits**
   - Always add `LIMIT $limit` clause
   - Default limit to 10 or 50
   - Prevents memory issues

3. **Avoid Unbounded Traversal**
   - Use `[*1..3]` instead of `[*]`
   - Bound path depth to 3-5 hops
   - Document depth restrictions

4. **Design for Reusability**
   - Make templates work across datasets
   - Parameterize all variable values
   - Use standard naming conventions

5. **Include Documentation**
   - Parameter descriptions
   - Example values
   - Performance characteristics

6. **Index Awareness**
   - Recommend indexes for filtered properties
   - Consider composite indexes
   - Document index creation

7. **Error Handling**
   - Validate parameter types
   - Handle null values
   - Provide default behaviors

8. **Template Versioning**
   - Track template versions
   - Support template evolution
   - Document changes

---

## 🔗 Integration with Other Skills

This skill integrates with:

- **graph-query-debugging-tool** - Debug generated templates
- **graph-query-optimization-assistant** - Optimize templates further
- **nl-to-graph-query-translator** - Translate natural language to templates
- **graph-schema-validation** - Validate templates against schema
- **multi-hop-reasoning-query-builder** - Build complex path templates

---

## 📚 Template Usage Scenarios

### Scenario 1: Web Application
```
Goal: Find user by email
Generated: SELECT ?user WHERE { ?user foaf:email $email }
Usage: Execute in REST API endpoint
```

### Scenario 2: Analytics Dashboard
```
Goal: Aggregate employee counts by company
Generated: Match relationships, group by company, count
Usage: Update dashboard monthly
```

### Scenario 3: Mobile App
```
Goal: Get person's network (friends and followers)
Generated: Multi-hop path template with depth limit
Usage: Paginated results in app
```

### Scenario 4: Data Export
```
Goal: Export all entities of type with properties
Generated: Complete node projection template
Usage: Scheduled export job
```

---

## 📖 Summary

This skill generates reusable graph query templates for common database operations.

It helps developers quickly scaffold Cypher or SPARQL queries, improving productivity and reducing query-writing effort through standardized, production-ready templates.

---

**Status: Enterprise-Grade Template Generation**

Comprehensive template library and generation system for professional knowledge graph development.