## Description:

Comprehensive Feishu/Lark integration guidance for OpenClaw agents covering messaging, group management, Bitable, documents, calendar, video conferencing, meeting minutes, tasks, approvals, contacts, cloud drive, and wiki workflows through the official Lark MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucascheung](https://clawhub.ai/user/lucascheung)

### License/Terms of Use:


## Use Case:

Developers and automation builders use this skill to configure an agent for Feishu/Lark workplace operations such as messaging, document handling, calendar coordination, task management, approvals, and knowledge-base access through Lark MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs mutable npm code while using Lark app credentials.

Mitigation: Pin and review the Lark MCP package version before use, and avoid passing app secrets directly on the command line.

Risk: The enabled Lark workflows can perform broad workplace read, write, and delete actions.

Mitigation: Grant only the Lark scopes required for the intended workflow and require explicit user confirmation before destructive actions.

Risk: The skill can guide access to sensitive workplace content such as recordings, transcripts, approvals, and private documents.

Mitigation: Limit access to approved workspaces and review sensitive outputs before sharing or acting on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lucascheung/skills/lark-mcp)
- [Publisher Profile](https://clawhub.ai/user/lucascheung)
- [Project Homepage](https://github.com/lucascheung/lark-mcp)
- [Lark OpenAPI MCP Server](https://github.com/larksuite/lark-openapi-mcp)
- [Lark Open Platform Documentation](https://open.larkoffice.com/document/home/index)
- [Lark Card Builder](https://open.larkoffice.com/cardkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Lark MCP server and LARK_APP_ID/LARK_APP_SECRET credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
