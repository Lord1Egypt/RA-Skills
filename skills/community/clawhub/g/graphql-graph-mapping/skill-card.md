## Description:

Maps GraphQL queries and schemas to graph database operations so applications can expose knowledge graph data through GraphQL APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design GraphQL API layers over graph databases and to translate GraphQL selections into Cypher, Gremlin, SPARQL, or property graph query patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated graph database queries may be unsafe when applied to sensitive or write-capable databases.

Mitigation: Review generated queries before execution, use authorized read-only and least-privilege database accounts, and require explicit approval for any write-capable operation.

Risk: Untrusted GraphQL input could be translated directly into backend database queries without adequate guardrails.

Mitigation: Do not expose the mapper directly to untrusted input; validate schemas and queries, constrain depth and complexity, and route execution through parameterized backend APIs.

## Reference(s):

- [GraphQL Graph Mapping - Design Patterns](references/graphql-mapping-patterns.md)
- [GraphQL Graph Mapping - Examples](examples/graphql-mapping-examples.md)
- [GraphQL Graph Mapping - Quick Reference](README.md)
- [ClawHub Skill Page](https://clawhub.ai/fisa712/skills/graphql-graph-mapping)
- [ClawHub Homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets and generated graph query text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Cypher, Gremlin, SPARQL, JSON response examples, schema mapping guidance, and implementation-oriented Python usage.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
