## Description:

Mail MCP helps agents install and use a mail MCP service to send, search, read, and manage emails and mail folders, including attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adjia](https://clawhub.ai/user/adjia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure a mail MCP server and perform email workflows such as sending messages, searching mail, reading messages, and managing folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs mutable remote code and the installer uses --break-system-packages.

Mitigation: Use a trusted, pinned version of the mail MCP server, prefer an isolated virtual environment, and avoid --break-system-packages.

Risk: The skill handles mailbox credentials that may be stored in plaintext configuration.

Mitigation: Use an app password or a secret manager instead of a primary mailbox password, and limit the mailbox account's privileges where possible.

Risk: The skill can send email and perform destructive or state-changing mailbox actions such as delete, move, and folder management.

Mitigation: Require explicit user confirmation before send, delete, move, or folder-management actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adjia/skills/mail-mcp)
- [mail-mcp-server project](https://github.com/AdJIa/mail-mcp-server)
- [Gmail App Password help](https://support.google.com/accounts/answer/185833)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands, JSON configuration examples, and MCP call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mailbox connection settings, MCP tool arguments, folder names, search filters, recipient lists, and attachment metadata.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
