## Description: <br>
Translate natural language questions into Cypher or SPARQL queries for graph databases and knowledge graphs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn natural language questions into graph query drafts for Neo4j-style property graphs and RDF knowledge graphs. It helps prototype Cypher and SPARQL queries, explanations, and parameter templates before review and execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Cypher or SPARQL may be too broad, inefficient, or mismatched to the target graph schema. <br>
Mitigation: Review each query before execution, validate it against the target schema, parameterize user values, and add LIMIT clauses for broad traversals. <br>
Risk: Mutating graph queries such as CREATE, SET, or DELETE can alter production data. <br>
Mitigation: Use read-only or least-privilege database roles by default, and require explicit approval and backups before running mutating examples on production data. <br>
Risk: Ambiguous natural language can lead to incorrect entity or relationship choices. <br>
Mitigation: Provide schema hints, clarify ambiguous entity names, and inspect the generated explanation before using the query. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fisa712/nl-to-graph-query-translator) <br>
- [ClawHub](https://clawhub.com) <br>
- [Query Patterns Reference](references/query-patterns.md) <br>
- [Cypher Query Guide](references/cypher-query-guide.md) <br>
- [SPARQL Query Guide](references/sparql-query-guide.md) <br>
- [Entity Recognition Pipeline](references/entity-recognition.md) <br>
- [Relationship Extraction](references/relationship-extraction.md) <br>
- [API Reference](references/api-reference.md) <br>
- [Known Limitations and Edge Cases](tests/edge-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Cypher and SPARQL query examples, parameter templates, and optional Python helper code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated graph queries should be reviewed, parameterized, and validated against the target schema before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
