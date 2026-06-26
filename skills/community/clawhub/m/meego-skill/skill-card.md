## Description: <br>
Meego Skill helps agents query and manage Feishu Project work items, statuses, comments, teams, schedules, views, charts, fields, and MQL searches through documented Meego commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longsasasasasa](https://clawhub.ai/user/longsasasasasa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, project teams, and agents use this skill to retrieve, create, update, transition, and comment on Feishu Project work items with step-by-step command guidance. It supports project administration workflows such as team lookup, schedule review, field discovery, chart inspection, and MQL-based filtering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags credential-handling guidance that may lead users to paste OAuth credentials, access tokens, or refresh tokens into chat. <br>
Mitigation: Provision credentials directly on the target host or through a secret manager, rotate any token already shared, and never paste credential files into chat. <br>
Risk: The skill can perform broad Feishu Project read/write actions, including comments, field updates, status transitions, and work-item creation. <br>
Mitigation: Use least-privilege Feishu credentials and require explicit user confirmation before any state-changing command is executed. <br>


## Reference(s): <br>
- [Meego MCP tools reference](references/tools.md) <br>
- [MQL query syntax reference](references/mql.md) <br>
- [Work item field configuration reference](references/fields.md) <br>
- [Feishu Project MCP endpoint](https://project.feishu.cn/mcp_server/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command examples for OAuth setup, Meego MCP calls, work item mutations, comments, field lookup, and troubleshooting.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
