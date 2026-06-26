# Parameterized Queries

This document demonstrates how to create reusable, secure parameterized queries with variable substitution.

## Why Parameterization?

**Security:** Prevents injection attacks  
**Reusability:** Use same query with different values  
**Performance:** Query plans can be cached  

---

## Basic Parameter Substitution

### Example 1: Simple Parameter

**Natural Language:**
```
Find employees at a given company
```

**Cypher (with parameters):**
```cypher
MATCH (e:Employee)-[:WORKS_AT]->(c:Company {name: $company_name})
RETURN e
```

**Parameters:**
```json
{
  "company_name": "Acme"
}
```

**Execution:**
```python
result = db.run(
    """
    MATCH (e:Employee)-[:WORKS_AT]->(c:Company {name: $company_name})
    RETURN e
    """,
    company_name="Acme"
)
```

---

### Example 2: Multiple Parameters

**Natural Language:**
```
Find employees at a company with salary greater than a threshold
```

**Cypher:**
```cypher
MATCH (e:Employee)-[:WORKS_AT]->(c:Company {name: $company_name})
WHERE e.salary > $min_salary
RETURN e
ORDER BY e.salary DESC
```

**Parameters:**
```json
{
  "company_name": "Acme",
  "min_salary": 60000
}
```

**Execution:**
```python
result = db.run(
    query,
    company_name="Acme",
    min_salary=60000
)
```

---

### Example 3: Numeric Ranges

**Natural Language:**
```
Find employees with salary within a range
```

**Cypher:**
```cypher
MATCH (e:Employee)
WHERE e.salary > $min_salary AND e.salary < $max_salary
RETURN e
ORDER BY e.salary
```

**Parameters:**
```json
{
  "min_salary": 40000,
  "max_salary": 80000
}
```

---

## Collection Parameters

### Example 4: IN with List

**Natural Language:**
```
Find employees in any of several departments
```

**Cypher:**
```cypher
MATCH (e:Employee)-[:IN_DEPARTMENT]->(d:Department)
WHERE d.name IN $department_names
RETURN e
```

**Parameters:**
```json
{
  "department_names": ["Sales", "Engineering", "Marketing"]
}
```

---

### Example 5: Match Any of Multiple Values

**Natural Language:**
```
Find companies with names matching any in a list
```

**Cypher:**
```cypher
MATCH (c:Company)
WHERE c.name IN $company_names
RETURN c
```

**Parameters:**
```json
{
  "company_names": ["Acme", "TechCorp", "GlobalSoft"]
}
```

---

## SPARQL Parameterization

### Example 6: SPARQL with Variables

**Natural Language:**
```
Find companies in a given industry
```

**SPARQL:**
```sparql
PREFIX ex: <http://example.com/>

SELECT ?company
WHERE {
  ?company rdf:type ex:Company .
  ?company ex:industry ?industry_var .
  FILTER (?industry_var = ?industry_param)
}
```

**Parameters:**
```json
{
  "industry_param": "Technology"
}
```

---

### Example 7: SPARQL VALUES Clause

**Natural Language:**
```
Find employees from a list of names
```

**SPARQL:**
```sparql
PREFIX ex: <http://example.com/>

SELECT ?employee
WHERE {
  ?employee rdf:type ex:Employee .
  ?employee foaf:name ?name .
  VALUES ?name { "Alice" "Bob" "Charlie" }
}
```

**Alternative with parameters:**
```sparql
PREFIX ex: <http://example.com/>

SELECT ?employee
WHERE {
  ?employee rdf:type ex:Employee .
  ?employee foaf:name ?name .
  FILTER (?name IN (?names_array))
}
```

---

## Template-Based Queries

### Example 8: Named Query Templates

**Template Definition:**
```python
QUERY_TEMPLATES = {
    "find_employee_at_company": """
        MATCH (e:Employee {name: $employee_name})-[:WORKS_AT]->(c:Company {name: $company_name})
        RETURN e, c
    """,
    
    "find_employees_by_salary": """
        MATCH (e:Employee)
        WHERE e.salary > $min_salary
        RETURN e
        ORDER BY e.salary DESC
        LIMIT $limit
    """,
    
    "find_colleagues": """
        MATCH (e:Employee {name: $employee_name})-[:WORKS_AT]->(c:Company)<-[:WORKS_AT]-(colleague:Employee)
        WHERE colleague.name <> $employee_name
        RETURN colleague
    """
}
```

**Usage:**
```python
def execute_template(template_name, **params):
    query = QUERY_TEMPLATES[template_name]
    return db.run(query, **params)

# Execute
result = execute_template("find_colleagues", 
                         employee_name="Alice")
```

---

### Example 9: Dynamic Query Builder

**Builder Pattern:**
```python
class QueryBuilder:
    def __init__(self, base_label):
        self.base_label = base_label
        self.filters = []
        self.params = {}
    
    def add_filter(self, property_name, operator, param_name, value):
        self.filters.append(f"n.{property_name} {operator} ${param_name}")
        self.params[param_name] = value
        return self
    
    def build(self):
        match_clause = f"MATCH (n:{self.base_label})"
        where_clause = "WHERE " + " AND ".join(self.filters) if self.filters else ""
        query = f"{match_clause}\n{where_clause}\nRETURN n" if where_clause else f"{match_clause}\nRETURN n"
        return query, self.params

# Usage
builder = QueryBuilder("Employee")
builder.add_filter("salary", ">", "min_sal", 60000)
builder.add_filter("department", "=", "dept", "Sales")
query, params = builder.build()

result = db.run(query, **params)
```

---

## Advanced Parameterization

### Example 10: Conditional Paths

**Natural Language:**
```
Find colleagues, optionally filtering by department
```

**Cypher:**
```cypher
MATCH (e:Employee {name: $employee_name})-[:WORKS_AT]->(c:Company)<-[:WORKS_AT]-(colleague:Employee)
WHERE (colleague.department = $department OR $department IS NULL)
  AND colleague.name <> $employee_name
RETURN colleague
```

**Usage:**
```python
# Find all colleagues
result = db.run(query, employee_name="Alice", department=None)

# Find colleagues in Sales only
result = db.run(query, employee_name="Alice", department="Sales")
```

---

### Example 11: Skip and Limit Parameters

**Natural Language:**
```
Paginate through results
```

**Cypher:**
```cypher
MATCH (e:Employee)
RETURN e
ORDER BY e.name
SKIP $offset
LIMIT $page_size
```

**Usage:**
```python
def get_employees_page(page_num, page_size=20):
    offset = (page_num - 1) * page_size
    return db.run(
        query,
        offset=offset,
        page_size=page_size
    )

# Get page 2
result = get_employees_page(2, page_size=50)
```

---

### Example 12: Dynamic Relationship Types

**Natural Language:**
```
Find connections through a specific relationship type
```

**Limitation:** Cypher doesn't directly support parameterizing relationship types in MATCH clauses. However, you can work around this:

**Cypher (Workaround):**
```cypher
MATCH (a:Person {name: $person_a})-[r]->(b:Person {name: $person_b})
WHERE type(r) = $relationship_type
RETURN r
```

**Parameters:**
```json
{
  "person_a": "Alice",
  "person_b": "Bob",
  "relationship_type": "KNOWS"
}
```

---

## Best Practices for Parameterized Queries

### ✅ DO

✓ Always use parameters for user input
```python
# Good
db.run("MATCH (n:Person {name: $name}) RETURN n", name=user_input)
```

✓ Use descriptive parameter names
```python
# Good
db.run(query, company_name="Acme", min_salary=50000)

# Less clear
db.run(query, {"a": "Acme", "b": 50000})
```

✓ Validate parameter types
```python
def get_employee_salary(min_salary: int, max_salary: int):
    if not isinstance(min_salary, int) or not isinstance(max_salary, int):
        raise TypeError("Salary must be integer")
    return db.run(query, min_salary=min_salary, max_salary=max_salary)
```

✓ Use NULL for optional parameters
```python
# Query
WHERE (n.department = $dept OR $dept IS NULL)

# Call without department filter
db.run(query, dept=None)
```

---

### ❌ DON'T

❌ String interpolation (SQL injection risk)
```python
# Bad
query = f"MATCH (n:Person {{name: '{user_name}'}}) RETURN n"
```

❌ Embed lists as strings
```python
# Bad
names = "Alice,Bob,Charlie"
query = f"WHERE n.name IN [{names}]"

# Good
names = ["Alice", "Bob", "Charlie"]
db.run("WHERE n.name IN $names", names=names)
```

❌ Parameterize relationship types (not directly supported)
```cypher
# Bad (doesn't work)
MATCH (a)-[:$rel_type]->(b)

# Good (workaround)
MATCH (a)-[r]->(b)
WHERE type(r) = $rel_type
```

---

## Security Considerations

### Example 13: Preventing Injection

**Vulnerable (without parameters):**
```python
# Danger: user input directly in query
user_name = request.get("name")
query = f"MATCH (n:Person {{name: '{user_name}'}}) RETURN n"
# If user_name = "'; DETACH DELETE (n); //"
# Query becomes: MATCH (n:Person {name: ''; DETACH DELETE (n); //'}}) RETURN n
```

**Safe (with parameters):**
```python
# Safe: parameterized
user_name = request.get("name")
query = "MATCH (n:Person {name: $name}) RETURN n"
result = db.run(query, name=user_name)
# Injection attempt is treated as literal string value
```

---

## Performance Considerations

### Example 14: Query Plan Caching

With parameterized queries, the database can reuse query execution plans:

```python
# Same query, different parameters
# Database can cache the execution plan

for user in users:
    result = db.run(
        "MATCH (u:User {id: $user_id}) RETURN u.name",
        user_id=user.id
    )
    # Query plan reused, faster execution
```

---

## SPARQL Parameter Examples

### Example 15: SPARQL with Property Path and Parameters

```sparql
PREFIX ex: <http://example.com/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?person ?distant
WHERE {
  ?person foaf:name ?person_name .
  FILTER (?person_name = ?name_param)
  
  ?person (foaf:knows+) ?distant .
  
  ?distant foaf:name ?distant_name .
  FILTER (regex(?distant_name, ?name_regex))
}
```

**Parameters:**
```json
{
  "name_param": "Alice",
  "name_regex": "^A.*"
}
```

---

## Summary

Parameterized queries provide:
- ✅ Security (prevents injection)
- ✅ Reusability (template-based)
- ✅ Performance (plan caching)
- ✅ Maintainability (clear separation of logic)

See [API Reference](../references/api-reference.md) for programmatic parameter handling.

