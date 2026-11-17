## Description:

A schema-aware Neo4j helper that detects graph structure and turns natural-language questions into Cypher queries with formatted results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffrao](https://clawhub.ai/user/jeffrao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to inspect a Neo4j graph schema, generate read-oriented Cypher from natural-language questions, troubleshoot query errors, and format graph query results for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Schema discovery and sample queries can expose sensitive graph labels, properties, relationships, or records.

Mitigation: Use a dedicated read-only Neo4j account with restricted labels, properties, and procedures, and avoid full-record sampling on sensitive databases.

Risk: Generated Cypher could be incorrect, expensive, or unsafe if execution safeguards are too weak.

Mitigation: Require query preview and approval before schema discovery or execution, enforce read-only operations, and keep strict LIMIT and path-depth controls.

Risk: Credentials or raw database responses could leak through logs or persistent memory.

Mitigation: Require HTTPS to a trusted endpoint and prevent credentials, full query responses, and sensitive sampled fields from being written to logs or memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeffrao/skills/neo4j-cypher-query-analyze)
- [Publisher profile](https://clawhub.ai/user/jeffrao)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Cypher, shell command, table, graph-path, statistics, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Neo4j connection environment variables and curl; may cache schema and query patterns in memory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
