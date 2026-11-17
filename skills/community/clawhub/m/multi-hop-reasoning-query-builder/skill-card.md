## Description:

Generate graph queries that perform multi-hop traversal and reasoning across relationships in graph databases and knowledge graphs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and graph engineers use this skill to create Cypher and SPARQL queries for multi-hop traversal, path discovery, indirect relationship detection, and knowledge graph exploration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Cypher, SPARQL, or index statements may not match the target graph schema or may be too expensive for production data.

Mitigation: Validate labels, relationship types, property names, hop counts, and limits against a trusted schema, then test with EXPLAIN/PROFILE or staging data before use.

Risk: Example domains such as healthcare, finance, fraud detection, and supply chain analysis may involve sensitive data.

Mitigation: Use only authorized datasets and apply appropriate privacy and access controls before adapting the generated queries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fisa712/skills/multi-hop-reasoning-query-builder)
- [Publisher Profile](https://clawhub.ai/user/fisa712)
- [Multi-Hop Reasoning Patterns](artifact/references/multi-hop-patterns.md)
- [Multi-Hop Reasoning Examples](artifact/examples/multi-hop-examples.md)
- [ClawHub Homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Cypher, SPARQL, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces query templates, path traversal examples, complexity notes, and performance recommendations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
