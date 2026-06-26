---
name: nl-to-graph-query-translator
description: Translate natural language questions into Cypher or SPARQL queries for graph databases and knowledge graphs.
metadata:
  {"openclaw":{"emoji":"🔍","homepage":"https://clawhub.com"}}
status: production
version: 1.0.0
tags: ["graph-queries", "nlp", "cypher", "sparql", "query-generation"]
---

# Natural Language → Cypher / SPARQL Translator

**Convert natural language questions into executable graph queries.**

This skill translates human-readable requests into graph query languages such as **Cypher** (Neo4j) or **SPARQL** (RDF), allowing developers to interact with graph databases using natural language instead of writing complex query syntax.

## Quick Start

### Use Cases

Use this skill when a user wants to:

- ✅ Convert natural language questions into graph queries
- ✅ Generate Cypher queries for property graph databases
- ✅ Generate SPARQL queries for RDF triple stores
- ✅ Explore graph datasets using plain English
- ✅ Quickly prototype graph queries

**Example requests:**
- "Find employees who work at Acme."
- "Show all companies located in California."
- "List people connected to Alice within two hops."
- "Find products purchased by customers in London."

### What This Skill Produces

The skill generates executable graph queries in supported query languages:

- 🔗 Cypher queries (Neo4j)
- 🔗 SPARQL queries (RDF triple stores)
- 📝 Query explanations
- 🎯 Query parameter templates

## Translation Process

The translator follows a 5-step process to convert natural language into executable queries:

1. **Identify Entities** — Detect entity names (people, organizations, locations)
2. **Identify Relationships** — Extract relationship verbs (works at, located in, purchased, etc.)
3. **Determine Query Type** — Classify request type (nodes, relationships, paths, counts, aggregations)
4. **Construct Query Pattern** — Build graph patterns representing relationships
5. **Generate Query Syntax** — Convert patterns into Cypher or SPARQL

For detailed information about each step, see [Query Translation Strategy](references/query-patterns.md#translation-strategy).

## Supported Query Languages

### Cypher
Used in **Neo4j** and other property graph databases.

**Example:**
```cypher
MATCH (p:Person)-[:PURCHASED]->(product:Product)
RETURN p, product
```

📖 See [Cypher Query Guide](references/cypher-query-guide.md)

### SPARQL
Used in **RDF triple stores** and knowledge graphs.

**Example:**
```sparql
SELECT ?person ?product
WHERE {
  ?person :purchased ?product .
}
```

📖 See [SPARQL Query Guide](references/sparql-query-guide.md)

## Common Patterns

### Simple Entity Lookup
```
"Find all people named Alice"
```

### Relationship Traversal
```
"Show companies where employees work"
```

### Multi-Hop Queries
```
"Find people connected to Alice within two relationships"
```

For more patterns, see [Query Patterns Reference](references/query-patterns.md).

## Examples

Browse practical examples organized by complexity and use case:

- 🚀 [Basic Translations](examples/basic-translations.md)
- 🔀 [Multi-Hop Queries](examples/multi-hop-queries.md)
- 🎯 [Parameterized Queries](examples/parameterized-queries.md)
- 📊 [Domain-Specific Examples](examples/domain-specific-examples.md)

## Best Practices

When generating and executing graph queries:

✓ Use schema labels consistently  
✓ Avoid overly broad relationship patterns  
✓ Prefer parameterized queries for security  
✓ Include LIMIT clauses for large datasets  
✓ Validate query syntax before execution  

See [Architecture & Implementation](architecture.md) for advanced considerations.

## Advanced Topics

- 🏗️ [System Architecture & Design](architecture.md)
- 🔧 [Entity Recognition Pipeline](references/entity-recognition.md)
- 🔗 [Relationship Extraction](references/relationship-extraction.md)
- 📚 [API Reference](references/api-reference.md)
- ⚠️ [Known Limitations & Edge Cases](tests/edge-cases.md)

## Related Skills

- [Graph Query Debugging Tool](../graph-query-debugging-tool/SKILL.md)
- [Graph Query Optimization Assistant](../graph-query-optimization-assistant/SKILL.md)
- [Graph Template Query Generator](../graph-template-query-generator/SKILL.md)
- [Multi-Hop Reasoning Query Builder](../multi-hop-reasoning-query-builder/SKILL.md)

---

**Last Updated:** 2026-03-08  
**Maintainer:** OpenClaw Community  
**License:** See LICENSE in repository root
