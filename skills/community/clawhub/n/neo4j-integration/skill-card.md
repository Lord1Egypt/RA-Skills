## Description:

Provides Neo4j and Cypher guidance, examples, and connector-style code for storing, querying, and managing knowledge graph data with the property graph model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft Cypher queries, model Neo4j graph data, and understand common database patterns for knowledge graph applications. It can also guide setup, transaction handling, indexing, bulk import, and result mapping work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled connector simulates Neo4j operations and may report success without proving that live database writes, deletes, transactions, or audits occurred.

Mitigation: Treat scripts/neo4j_connector.py as mock or demo code and validate any production connector against the official Neo4j driver and a non-production database before live use.

Risk: Cypher examples include destructive delete patterns and import/export operations that can affect live graph data or expose approved data paths if copied directly.

Mitigation: Use least-privilege credentials, test on non-production data, confirm DELETE or DETACH DELETE targets, and restrict APOC exports to approved data and paths.

Risk: Example connection snippets include placeholder passwords that could encourage hardcoded credentials.

Mitigation: Replace sample credentials with managed secrets or environment-specific credential handling before running against a real Neo4j instance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fisa712/skills/neo4j-integration)
- [Neo4j Integration - Design Patterns](artifact/references/neo4j-patterns.md)
- [Neo4j Integration - Examples](artifact/examples/neo4j-examples.md)
- [ClawHub](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Cypher and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database query examples, connector usage notes, configuration snippets, and security guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
