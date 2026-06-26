# NL-to-Graph-Query-Translator Skill Repository

Welcome to the modularized repository structure for the Natural Language to Graph Query Translator skill!

## 📁 Repository Structure

```
nl-to-graph-query-translator/
│
├── SKILL.md                          # Main skill overview & quick reference
├── architecture.md                   # System design & architecture
│
├── references/                       # Technical reference documentation
│   ├── cypher-query-guide.md         # Cypher syntax and patterns
│   ├── sparql-query-guide.md         # SPARQL syntax and patterns
│   ├── query-patterns.md             # Translation patterns & mapping
│   ├── entity-recognition.md         # Entity extraction pipeline
│   ├── relationship-extraction.md    # Relationship identification
│   └── api-reference.md              # API functions & data models
│
├── examples/                         # Practical, runnable examples
│   ├── basic-translations.md         # Simple NL→Query examples
│   ├── multi-hop-queries.md          # Complex path traversal
│   ├── parameterized-queries.md      # Reusable query templates
│   └── domain-specific-examples.md   # HR, E-commerce, Healthcare, etc.
│
├── tests/                            # Testing & validation
│   └── edge-cases.md                 # Known limitations & workarounds
│
└── scripts/                          # Helper utilities (future)
    ├── query-validator.py
    ├── schema-parser.py
    └── test-translator.py
```

## 📚 Quick Navigation

### For Getting Started
- Start with **[SKILL.md](SKILL.md)** for overview and use cases
- See **[Basic Translations](examples/basic-translations.md)** for simple examples

### For Learning Query Syntax
- **[Cypher Query Guide](references/cypher-query-guide.md)** – Neo4j query language
- **[SPARQL Query Guide](references/sparql-query-guide.md)** – RDF query language

### For Understanding How It Works
- **[Query Patterns Reference](references/query-patterns.md)** – Translation strategy
- **[Entity Recognition](references/entity-recognition.md)** – NER pipeline
- **[Relationship Extraction](references/relationship-extraction.md)** – RE pipeline

### For Building Applications
- **[API Reference](references/api-reference.md)** – Function signatures & usage
- **[Architecture](architecture.md)** – System design & integration points

### For Advanced Scenarios
- **[Multi-Hop Queries](examples/multi-hop-queries.md)** – Complex traversals
- **[Parameterized Queries](examples/parameterized-queries.md)** – Reusable templates
- **[Domain-Specific Examples](examples/domain-specific-examples.md)** – Real-world use cases

### For Troubleshooting
- **[Edge Cases & Limitations](tests/edge-cases.md)** – Known issues & workarounds

---

## 🚀 Quick Start

### Translate a Simple Query

**Natural Language:**
```
Find employees who work at Acme
```

**Generated Cypher:**
```cypher
MATCH (e:Employee)-[:WORKS_AT]->(c:Company {name: "Acme"})
RETURN e
```

**Generated SPARQL:**
```sparql
SELECT ?employee
WHERE {
  ?employee rdf:type ex:Employee .
  ?employee ex:works_at ex:Acme .
}
```

### Try More Examples
- See [Basic Translations](examples/basic-translations.md) for 15+ simple examples
- See [Domain-Specific Examples](examples/domain-specific-examples.md) for 26 real-world scenarios

---

## 📖 Key Concepts

### Translation Process

The skill follows a **5-step pipeline**:

1. **Entity Extraction** – Identify nouns/named entities (people, companies, etc.)
2. **Relationship Extraction** – Identify verbs/connections between entities
3. **Intent Classification** – Determine query type (find, count, exists, path, etc.)
4. **Query Pattern Building** – Construct abstract query pattern
5. **Query Generation** – Convert pattern to Cypher/SPARQL syntax

### Supported Query Languages

| Language | Use Case | Database |
|----------|----------|----------|
| **Cypher** | Property graphs | Neo4j, others |
| **SPARQL** | RDF triple stores | Virtuoso, Jena, etc. |

### Key Features

✅ Automatic entity recognition  
✅ Relationship type inference  
✅ Multi-hop path queries  
✅ Aggregation & grouping  
✅ Parameterized queries  
✅ Query validation  
✅ Alternative query suggestions  

---

## 🔍 Documentation Map

### By Task

**I want to:**
- ➜ **Understand the skill** → Read [SKILL.md](SKILL.md)
- ➜ **Write Cypher queries** → See [Cypher Query Guide](references/cypher-query-guide.md)
- ➜ **Write SPARQL queries** → See [SPARQL Query Guide](references/sparql-query-guide.md)
- ➜ **See examples** → Browse [Examples](examples/)
- ➜ **Use the API** → Read [API Reference](references/api-reference.md)
- ➜ **Understand translation** → Study [Query Patterns](references/query-patterns.md)
- ➜ **Build a system** → Review [Architecture](architecture.md)
- ➜ **Debug issues** → Check [Edge Cases](tests/edge-cases.md)

### By Role

**Developer:**
- API Reference
- Examples
- Architecture

**Data Analyst:**
- Query Pattern Reference
- Query Language Guides
- Domain-Specific Examples

**System Architect:**
- Architecture Document
- Integration Points
- Performance Considerations

**QA Engineer:**
- Edge Cases & Limitations
- Testing Strategy
- Known Issues

---

## 📋 Reference Tables

### Common Entity Types

| Type | Examples | Label |
|------|----------|-------|
| Person | Alice, Bob, John Smith | Person, Employee, Manager |
| Organization | Acme, Google, Microsoft | Company, Department |
| Location | New York, California | City, Country, Region |
| Product | iPhone, Database | Product, Service |

### Common Relationship Types

| Phrase | Type | Direction |
|--------|------|-----------|
| works at | WORKS_AT | → |
| knows | KNOWS | ↔ |
| located in | LOCATED_IN | → |
| owns | OWNS | → |
| manages | MANAGES | → |

See [Entity Recognition](references/entity-recognition.md#entity-recognition-patterns) and [Relationship Extraction](references/relationship-extraction.md#mapping-table) for complete tables.

---

## 🎯 Common Patterns

### Simple Lookup
```
"Find all people named Alice"
```
See: [Basic Translations](examples/basic-translations.md#example-1-find-person-by-name)

### Relationship Traversal
```
"Show companies where employees work"
```
See: [Basic Translations](examples/basic-translations.md#example-4-find-related-nodes)

### Multi-Hop Traversal
```
"Find friends of friends"
```
See: [Multi-Hop Queries](examples/multi-hop-queries.md#example-1-find-friends-of-friends)

### Aggregation
```
"Count employees by department"
```
See: [Basic Translations](examples/basic-translations.md#example-8-count-results)

### Parameterized Query
```
"Find employees at a given company"
```
See: [Parameterized Queries](examples/parameterized-queries.md#example-1-simple-parameter)

---

## ⚙️ Integration

### With Neo4j
Use generated Cypher queries directly with Neo4j driver.

### With RDF Stores
Use generated SPARQL queries with any SPARQL endpoint.

### With Custom Backends
Implement new generator following [Architecture](architecture.md).

---

## 🔧 Configuration

### Adding Custom Entity Types
See [Entity Recognition](references/entity-recognition.md#step-3-entity-classification)

### Adding Domain Vocabulary
See [Relationship Extraction](references/relationship-extraction.md#mapping-table)

### Customizing Query Generation
See [Architecture](architecture.md#extensibility)

---

## ✅ Validation Checklist

When translating natural language:

- ✓ Are entities recognized correctly?
- ✓ Are relationships identified accurately?
- ✓ Is relationship direction correct?
- ✓ Are filters applied properly?
- ✓ Is the query performant?
- ✓ Are results within expected scope?

See [Validation Strategy](tests/edge-cases.md#testing-strategy) for detailed testing.

---

## 🆘 Troubleshooting

### Query Returns No Results
- Check entity spelling
- Verify entities exist in database
- Check relationship types

### Query Times Out
- Limit path length: `[*1..5]` instead of `[*]`
- Add more specific filters
- Use `LIMIT` clause

### Ambiguous Results
- Be more specific in natural language
- Provide schema hints
- Check [Edge Cases](tests/edge-cases.md)

---

## 📞 Related Skills

This skill integrates with:
- [Graph Query Debugging Tool](../graph-query-debugging-tool/SKILL.md)
- [Graph Query Optimization Assistant](../graph-query-optimization-assistant/SKILL.md)
- [Graph Template Query Generator](../graph-template-query-generator/SKILL.md)
- [Multi-Hop Reasoning Query Builder](../multi-hop-reasoning-query-builder/SKILL.md)

---

## 📝 File Guide

| File | Purpose | Audience |
|------|---------|----------|
| SKILL.md | Overview & quick start | Everyone |
| architecture.md | System design | Architects, Developers |
| cypher-query-guide.md | Cypher reference | Developers, Analysts |
| sparql-query-guide.md | SPARQL reference | Developers, Analysts |
| query-patterns.md | Translation strategy | Developers, Contributors |
| entity-recognition.md | Entity extraction | Developers, ML Engineers |
| relationship-extraction.md | Relationship extraction | Developers, ML Engineers |
| api-reference.md | API documentation | Developers |
| basic-translations.md | Simple examples | Everyone |
| multi-hop-queries.md | Complex examples | Developers, Analysts |
| parameterized-queries.md | Reusable patterns | Developers |
| domain-specific-examples.md | Real-world use cases | Business users, Analysts |
| edge-cases.md | Limitations & workarounds | QA, Developers |

---

## 🔄 Contribution Guidelines

When contributing:

1. **Update relevant documentation** in `references/` or `examples/`
2. **Add test cases** to `tests/edge-cases.md`
3. **Follow naming conventions** from [Query Patterns](references/query-patterns.md)
4. **Update [SKILL.md](SKILL.md)** if adding major features
5. **Test against multiple backends** (Neo4j, RDF stores)

---

## 📄 License

This skill is part of the OpenClaw Knowledge Graph project. See LICENSE in repository root.

---

## 🎓 Learning Path

**Beginner:**
1. Read [SKILL.md](SKILL.md)
2. Study [Basic Translations](examples/basic-translations.md)
3. Try simple queries

**Intermediate:**
1. Learn [Query Patterns](references/query-patterns.md)
2. Study [Multi-Hop Queries](examples/multi-hop-queries.md)
3. Explore [Domain Examples](examples/domain-specific-examples.md)

**Advanced:**
1. Read [Architecture](architecture.md)
2. Study [Entity Recognition](references/entity-recognition.md)
3. Study [Relationship Extraction](references/relationship-extraction.md)
4. Review [API Reference](references/api-reference.md)

---

**Last Updated:** 2026-03-08  
**Maintainer:** OpenClaw Community

