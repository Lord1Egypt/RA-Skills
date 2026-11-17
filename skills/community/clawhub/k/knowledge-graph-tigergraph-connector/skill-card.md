## Description:

Connect to TigerGraph distributed graph database to query, load, and manage large-scale knowledge graph data using GSQL and REST++ APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to connect agents to TigerGraph workflows for graph querying, data loading, schema guidance, graph algorithms, and knowledge graph management. Review the included connector before using it with real TigerGraph environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary says the skill presents mock database operations as production-ready.

Mitigation: Treat the included Python connector as scaffold code until real authentication, query execution, CSV parsing, error handling, and verification are implemented.

Risk: The server security summary flags broad database write and schema guidance without clear safeguards.

Mitigation: Use least-privilege TigerGraph credentials, test against non-production graphs first, and require explicit approval for inserts, schema changes, and index changes.

Risk: The skill can guide agents through operations that affect graph data and schemas.

Mitigation: Pin dependencies in an isolated environment and review generated GSQL, REST++ calls, and data-loading steps before execution.

## Reference(s):

- [TigerGraph GSQL Design Patterns](artifact/references/tigergraph-patterns.md)
- [TigerGraph Official Documentation](https://docs.tigergraph.com/)
- [GSQL Reference](https://docs.tigergraph.com/gsql-ref/current/)
- [REST++ API Guide](https://docs.tigergraph.com/api/rest-api/)
- [Python pyTigerGraph](https://pytigergraph.github.io/intro/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON, Python, GSQL, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include TigerGraph connection settings, GSQL query examples, graph loading examples, and operational guidance.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
