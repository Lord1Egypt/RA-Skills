## Description:

Structural database health scanner that audits schema topology for orphaned tables, missing indexes, nullable foreign keys, circular dependencies, and related issues without reading row data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nlr-ai](https://clawhub.ai/user/nlr-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use GraphCare through an MCP-capable agent to audit PostgreSQL, MySQL, or SQLite schema topology for structural problems before they affect performance or integrity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SQLite identifier handling flaws and vulnerable database dependencies may affect scan reliability or package safety.

Mitigation: Review the package before installation and prefer an updated release that fixes SQLite identifier handling and vulnerable dependencies.

Risk: Using privileged credentials or untrusted database targets can increase exposure when running a scanner with database connectivity.

Mitigation: Use read-only database credentials and avoid pointing the skill at untrusted MySQL servers or SQLite files.

## Reference(s):

- [GraphCare ClawHub skill page](https://clawhub.ai/nlr-ai/skills/graphcare)
- [GraphCare homepage](https://github.com/mind-protocol/graphcare)
- [Publisher profile](https://clawhub.ai/user/nlr-ai)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [MCP tool responses containing JSON audit reports or plain-text finding explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit reports include detected tables, findings, metrics, and a health score.]

## Skill Version(s):

1.0.0 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
