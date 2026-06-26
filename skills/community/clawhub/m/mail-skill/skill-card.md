## Description: <br>
Helps agents configure and use a Mail MCP service to send, search, organize, and manage email with support for folders, flags, replies, forwards, and attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdJIa](https://clawhub.ai/user/AdJIa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to a mailbox through mail-mcp, configure IMAP/SMTP settings, and perform common email workflows such as searching, sending, replying, forwarding, moving, and deleting messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, send, move, and delete mail through a configured mailbox. <br>
Mitigation: Use a dedicated mailbox or app-specific password and require manual confirmation before sending, forwarding, deleting, moving, or changing folders. <br>
Risk: The installer can fetch an unpinned mail-mcp dependency from an upstream GitHub repository. <br>
Mitigation: Review or pin the upstream dependency before installation, and install only when the upstream project is trusted. <br>
Risk: Mailbox credentials are required for IMAP and SMTP access. <br>
Mitigation: Prefer app-specific credentials with the minimum practical mailbox scope, and avoid using a primary account password. <br>


## Reference(s): <br>
- [Mail Skill on ClawHub](https://clawhub.ai/AdJIa/mail-skill) <br>
- [mail-mcp-server project](https://github.com/AdJIa/mail-mcp-server) <br>
- [Google Account App Passwords](https://support.google.com/accounts/answer/185833) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce mailbox operation commands that should be manually confirmed before sending, forwarding, deleting, moving, or changing folders.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
