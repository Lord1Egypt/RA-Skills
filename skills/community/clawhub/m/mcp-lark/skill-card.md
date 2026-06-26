## Description: <br>
Based on FeiShu / Lark's OpenAPI MCP server, this skill helps agents manage user information, chats, emails, cloud documents, multidimensional tables, tasks, calendars, and related workspace operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[al-one](https://clawhub.ai/user/al-one) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace operators use this skill to configure Lark or Feishu MCP server URLs and let an agent list schemas or call available OpenAPI-backed tools for collaboration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured MCP service URLs can grant broad access to Lark or Feishu workspace data. <br>
Mitigation: Use narrowly scoped MCP service URLs and only enable services needed for the current workflow. <br>
Risk: LARK_MCP_SERVERS may contain sensitive MCP URLs that should not be exposed. <br>
Mitigation: Treat LARK_MCP_SERVERS as a secret, store it outside committed files, and keep .env out of version control. <br>
Risk: The skill can support sending messages, editing documents, and changing tasks or calendars. <br>
Mitigation: Require manual confirmation before actions that send, edit, delete, or modify workspace content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/al-one/mcp-lark) <br>
- [Lark MCP remote mode documentation](https://open.larksuite.com/document/mcp_open_tools/call-feishu-mcp-server-in-remote-mode) <br>
- [Feishu MCP remote mode documentation](https://open.feishu.cn/document/mcp_open_tools/end-user-call-remote-mcp-server) <br>
- [Sent message content](references/message_create.md) <br>
- [Lark message content documentation](https://open.larksuite.com/document/server-docs/im-v1/message-content-description/create_json?lang=en-US) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call configured Lark or Feishu MCP tools through mcporter when the user authorizes workspace actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
