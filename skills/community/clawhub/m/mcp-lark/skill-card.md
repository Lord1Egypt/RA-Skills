## Description:

Based on FeiShu / Lark's OpenAPI MCP server, this skill helps agents manage user information, chats, emails, cloud documents, multidimensional tables, tasks, calendars, and related workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[al-one](https://clawhub.ai/user/al-one)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to connect an agent to configured Lark or Feishu MCP service URLs and inspect or call the available OpenAPI-backed tools for collaboration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured Lark or Feishu MCP URLs can grant broad enterprise access to chats, mail, documents, calendars, tasks, and related data.

Mitigation: Use narrowly scoped MCP service URLs and install only in workspaces where that level of access is acceptable.

Risk: Token-bearing MCP URLs may be stored in `.env`.

Mitigation: Keep `.env` out of version control and rotate any exposed MCP URLs or tokens.

Risk: The skill recommends using an unpinned npm command for `mcporter`.

Mitigation: Prefer a pinned or preinstalled `mcporter` version before using the skill in routine workflows.

Risk: Agent actions may send, edit, or modify Lark or Feishu resources.

Mitigation: Confirm recipients, content, and target resources before any send, edit, file, mail, document, calendar, or task action.

## Reference(s):

- [Lark MCP remote server documentation](https://open.larksuite.com/document/mcp_open_tools/call-feishu-mcp-server-in-remote-mode)
- [Feishu MCP remote server documentation](https://open.feishu.cn/document/mcp_open_tools/end-user-call-remote-mcp-server)
- [Sent message content](references/message_create.md)
- [Lark message content documentation](https://open.larksuite.com/document/server-docs/im-v1/message-content-description/create_json?lang=en-US)
- [ClawHub skill page](https://clawhub.ai/al-one/skills/mcp-lark)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents to list MCP tools, inspect tool schemas, and call selected Lark or Feishu MCP tools.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
