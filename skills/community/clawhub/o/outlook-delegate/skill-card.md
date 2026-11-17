## Description:

Read, search, send, and manage Outlook mail and calendar through Microsoft Graph API with delegate support for sending as self, as owner, or on behalf of owner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[87marc](https://clawhub.ai/user/87marc)

### License/Terms of Use:

MIT

## Use Case:

Employees, administrators, and teams with Microsoft 365 delegate arrangements use this skill to let an agent operate a delegated Outlook mailbox and calendar. It is suited to assistant workflows where the mailbox owner has explicitly granted access and selected the intended sending mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests and persists broad Microsoft Graph authority for delegated mail and calendar access.

Mitigation: Install only when delegated Outlook access is intended, reduce Graph scopes where possible, protect ~/.outlook-mcp from backups or sync, and revoke Microsoft 365 and Exchange permissions when access is no longer needed.

Risk: The token-printing command can expose an access token in shell history, terminal logs, or automation logs.

Mitigation: Do not run token-printing commands in logged environments and treat generated OAuth tokens as secrets.

Risk: Mail and calendar commands can delete, move, update, or send items from a delegated mailbox.

Mitigation: Verify item IDs carefully before delete, move, update, or send-draft actions and review destructive actions before execution.

Risk: Granting both SendAs and SendOnBehalf can cause Exchange to use SendAs and hide the delegated sender indication.

Mitigation: Choose exactly one sending mode and avoid granting both SendAs and SendOnBehalf permissions.

## Reference(s):

- [Delegate Setup Guide](references/setup.md)
- [Outlook Delegate release page](https://clawhub.ai/87marc/skills/outlook-delegate)
- [Original Outlook skill](https://clawhub.ai/jotamed/outlook)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command invocations, JSON configuration examples, and script output from Microsoft Graph operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Microsoft 365 configuration, OAuth tokens, and Exchange delegate permissions.]

## Skill Version(s):

1.1.1 (source: server release evidence; artifact metadata/frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
