## Description:

Generate reusable Cypher or SPARQL query templates for common graph database operations such as finding nodes, relationships, paths, and aggregations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold reusable Cypher or SPARQL templates for node lookup, relationship traversal, path discovery, filtering, aggregation, and graph exploration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Cypher or SPARQL may include labels, relationship types, property names, operators, predicates, or traversal depth values that are unsuitable for a production graph schema.

Mitigation: Validate generated query structure against the application schema and allowlist acceptable labels, relationships, properties, predicates, operators, and traversal depths before use.

Risk: Starter examples may be copied into workflows that handle sensitive data without appropriate controls.

Mitigation: Apply authorization, minimization, auditing, and access controls before adapting templates to sensitive datasets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fisa712/skills/graph-template-query-generator)
- [ClawHub homepage](https://clawhub.com)
- [Template patterns](references/template-patterns.md)
- [Template examples](examples/template-examples.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with Cypher, SPARQL, JSON, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs commonly include a query template, parameter list, plain-English explanation, usage example, and performance notes.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
