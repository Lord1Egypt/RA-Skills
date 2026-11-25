## Description:

Designs and queries LadybugDB graphs with openCypher. Use for schemas, imports, query debugging, transactions, full-text search and Neo4j query adaptation, with local Python helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardodpalmeida](https://clawhub.ai/user/ricardodpalmeida)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to model and query LadybugDB property graphs, adapt Cypher workflows, troubleshoot results, and perform authorized database changes with local Python helpers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses local file and shell capabilities, and the scan did not verify the host runtime's permission enforcement.

Mitigation: Review the host permissions and the skill's file and shell behavior before use; keep database paths and queries within the intended scope.

Risk: The skill depends on a separately installed LadybugDB Python package.

Mitigation: Review and install the pinned ladybug==0.21.2 dependency only in the intended Python environment.

## Reference(s):

- [LadybugDB openCypher package](https://clawhub.ai/ricardodpalmeida/skills/ladybug-opencypher-updated)
- [Upstream Ladybug openCypher skill](https://clawhub.ai/trenza1ore/skills/ladybug-opencypher)
- [API reference](references/api-reference.md)
- [Workflow patterns](references/workflow-patterns.md)
- [LadybugDB Python client API](https://docs.ladybugdb.com/client-apis/python/)
- [LadybugDB migration guide](https://docs.ladybugdb.com/migrate/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Analysis]

**Output Format:** [Markdown guidance with Python, Cypher, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a structured report of database path, access mode, query counts, read-back checks, and unresolved limits.]

## Skill Version(s):

1.1.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
