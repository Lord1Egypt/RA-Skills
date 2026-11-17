## Description:

Meego Skill helps agents query and manage Feishu Project work items, workflow states, teams, schedules, comments, views, charts, fields, and MQL searches through OAuth-protected CLI calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longsasasasasa](https://clawhub.ai/user/longsasasasasa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project operators, and agent users use this skill to inspect and update Feishu Project work items, comments, schedules, fields, teams, views, charts, and MQL queries. It is intended for OAuth-authorized Meego project-management workflows that may include both read and write actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth credential files or tokens could be exposed if users paste credentials into chat or store them with broad access.

Mitigation: Do not paste OAuth credentials into AI chats; use secure transfer or a secret manager, restrictive file permissions, least-privilege scopes, and a dedicated service account where possible.

Risk: Privileged or unpinned npm installation patterns can increase supply-chain and host-permission exposure.

Mitigation: Use pinned package versions, review package sources before deployment, and run the tooling under an unprivileged runtime user.

Risk: The skill supports write actions such as adding comments, updating fields, creating work items, and changing workflow states.

Mitigation: Require user confirmation before write operations and verify project keys, work item IDs, target fields, permissions, and intended state transitions.

## Reference(s):

- [Meego Work Item Fields Reference](references/fields.md)
- [MQL Query Syntax Reference](references/mql.md)
- [Meego MCP Tools Reference](references/tools.md)
- [Feishu Project MCP Server](https://project.feishu.cn/mcp_server/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide OAuth setup and produce command arguments for Meego read and write operations.]

## Skill Version(s):

2.2.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
