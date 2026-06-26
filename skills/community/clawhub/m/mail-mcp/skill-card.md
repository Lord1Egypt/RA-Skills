## Description: <br>
Mail MCP helps agents install and use a mail MCP server to send, search, read, and manage email messages and folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdJIa](https://clawhub.ai/user/AdJIa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and email automation users use this skill to configure an MCP-accessible mailbox and perform common email workflows such as sending messages, searching mail, handling attachments, and managing folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant an agent broad mailbox control, including sending, forwarding, deleting, moving, and changing folders. <br>
Mitigation: Use an app-specific or limited mailbox credential and require manual confirmation before any send, forward, delete, move, or folder-changing operation. <br>
Risk: The install path pulls unpinned remote code for the mail MCP server. <br>
Mitigation: Review or pin the upstream mail-mcp-server code before installation, and install it in an isolated environment. <br>
Risk: Mailbox credentials are supplied through environment or local configuration. <br>
Mitigation: Protect the MCP configuration file, avoid using a primary account password when provider-specific app credentials are available, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [Mail MCP server project](https://github.com/AdJIa/mail-mcp-server) <br>
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes mailbox configuration guidance, MCP tool examples, and structured error-response examples.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
