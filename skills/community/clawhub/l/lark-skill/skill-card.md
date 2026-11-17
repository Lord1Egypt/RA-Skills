## Description:

Comprehensive Feishu/Lark integration skill for OpenClaw covering messaging, group management, Bitable, documents, calendar, video conferencing, meeting minutes, task management, approvals, contacts, cloud drive, wiki, and knowledge base workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucascheung](https://clawhub.ai/user/lucascheung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace automation teams use this skill to help OpenClaw agents operate Feishu/Lark workspaces through the official Lark MCP server. It supports common collaboration workflows across messages, chats, tables, documents, calendars, meetings, tasks, approvals, contacts, drive, and wiki resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad Feishu/Lark workspace authority across messages, files, meetings, calendars, approvals, and user data.

Mitigation: Grant only the scopes needed for the planned workflow, prefer app identity or read-only scopes where possible, and review requested operations before use.

Risk: Setup examples pass app credentials through shell commands and the MCP server depends on an external package.

Mitigation: Avoid typing secrets directly into shell history, protect and rotate the app secret, revoke unused user tokens, and pin and verify the MCP package version before deployment.

Risk: Supported operations include destructive or sensitive actions such as deleting data, changing permissions, forwarding content, managing approvals, and accessing recordings or transcripts.

Mitigation: Require explicit human confirmation before destructive, permission-changing, approval, forwarding, live-meeting, recording, or transcript access actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucascheung/skills/lark-skill)
- [Skill homepage](https://github.com/lucascheung/lark_skill)
- [Official Feishu/Lark OpenAPI MCP server](https://github.com/larksuite/lark-openapi-mcp)
- [Lark Open Platform documentation](https://open.larkoffice.com/document/home/index)
- [Lark Card Builder](https://open.larkoffice.com/cardkit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML-style API parameters and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured official Lark MCP server and Feishu/Lark app credentials.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
