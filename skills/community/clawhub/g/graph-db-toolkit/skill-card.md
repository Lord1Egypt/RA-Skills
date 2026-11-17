## Description:

Graph database toolkit for Neo4j and Cypher-based graph analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to work with Neo4j graph databases, build Cypher queries, perform CRUD operations, and run graph analytics for knowledge graphs, relationship analysis, recommendations, and traversal tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The toolkit can write to Neo4j databases and includes full-delete behavior.

Mitigation: Use a dedicated least-privileged Neo4j account and install the skill only for databases the agent is allowed to read and modify.

Risk: Example credentials and raw Cypher interfaces can be misused if copied into sensitive environments.

Mitigation: Change example passwords before use and treat raw Cypher or query-builder inputs as trusted-code interfaces rather than user-provided text.

Risk: Production data could be damaged if destructive helpers are available without guardrails.

Mitigation: Avoid production data until delete_all() is removed, guarded, or otherwise restricted by operational controls.

## Reference(s):

- [Cypher Cheatsheet](references/cypher_cheatsheet.md)
- [Neo4j Design Patterns](references/neo4j_patterns.md)
- [Graph DB Toolkit on ClawHub](https://clawhub.ai/kaiyuelv/skills/graph-db-toolkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Python, Cypher, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Neo4j connection guidance, generated Cypher queries, Python code snippets, graph analytics results, and configuration advice.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
