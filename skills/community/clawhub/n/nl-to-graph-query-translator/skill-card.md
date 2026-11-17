## Description:

Translate natural language questions into Cypher or SPARQL queries for graph databases and knowledge graphs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft Cypher or SPARQL queries, explanations, and parameter templates from natural-language questions while prototyping or exploring graph databases and knowledge graphs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Cypher or SPARQL can become executable database access if connected directly to a graph database.

Mitigation: Treat outputs as draft text; review, parse, and enforce a read-only policy before execution.

Risk: Queries may expose sensitive data or perform mutating or administrative operations if run with broad credentials.

Mitigation: Use least-privilege read-only credentials by default and require separate authorization and confirmation for mutating or administrative clauses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fisa712/skills/nl-to-graph-query-translator)
- [fisa712 publisher profile](https://clawhub.ai/user/fisa712)
- [ClawHub homepage](https://clawhub.com)
- [Cypher Query Guide](references/cypher-query-guide.md)
- [SPARQL Query Guide](references/sparql-query-guide.md)
- [Query Patterns Reference](references/query-patterns.md)
- [Entity Recognition Pipeline](references/entity-recognition.md)
- [Relationship Extraction](references/relationship-extraction.md)
- [API Reference](references/api-reference.md)
- [Known Limitations and Edge Cases](tests/edge-cases.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown containing generated Cypher or SPARQL snippets, explanations, and parameter templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated queries should be reviewed before execution; examples emphasize parameterization and LIMIT clauses.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
