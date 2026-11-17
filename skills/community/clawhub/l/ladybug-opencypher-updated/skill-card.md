## Description:

Designs and queries LadybugDB graphs with openCypher. Use for schemas, imports, query debugging, transactions, full-text search and Neo4j query adaptation, with local Python helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardodpalmeida](https://clawhub.ai/user/ricardodpalmeida)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design and query LadybugDB property graphs, import data, troubleshoot Cypher, and adapt Neo4j queries. It provides Python and shell helpers with read-only defaults and steps for authorized, verified writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benign security verdict is not a guarantee of zero risk.

Mitigation: Before installing, check whether the skill's declared scope and file and shell capabilities fit your needs.

Risk: Cypher imports, procedures, and extensions can reach host files or network resources; read-only database access does not restrict those capabilities.

Mitigation: Review COPY, LOAD, CALL, extensions, and paths, and use trusted absolute import paths.

Risk: Authorized write operations can change graph data, and statements outside an explicit transaction may commit separately.

Mitigation: Use writes only with authorization, group related changes in a transaction, and read back properties, direction, and identity.

## Reference(s):

- [LadybugDB package on ClawHub](https://clawhub.ai/ricardodpalmeida/skills/ladybug-opencypher-updated)
- [Upstream Ladybug openCypher skill](https://clawhub.ai/trenza1ore/skills/ladybug-opencypher)
- [Ladybug Python and Cypher API reference](references/api-reference.md)
- [Ladybug workflow patterns](references/workflow-patterns.md)
- [Official Ladybug Python API documentation](https://docs.ladybugdb.com/client-apis/python/)
- [Ladybug installation guide](https://docs.ladybugdb.com/installation/)
- [Ladybug Cypher differences from Neo4j](https://docs.ladybugdb.com/cypher/difference/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Cypher, Python, and shell code blocks; query result summaries and verification checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local database operations; query helper is read-only by default, and writes require explicit authorization.]

## Skill Version(s):

1.1.7 (source: changelog, released 2026-11-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
