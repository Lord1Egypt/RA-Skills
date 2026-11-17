## Description:

Read, search, organise, and draft emails using neomutt - a terminal IMAP client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elmoyeldo](https://clawhub.ai/user/elmoyeldo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate an IMAP mailbox from the terminal: list and search messages, read HTML mail, manage folders, archive messages, and compose drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup example stores an IMAP password directly in the NeoMutt configuration.

Mitigation: Use an app-specific token retrieved from a password manager or OS keychain where possible, and restrict permissions on the mail configuration files.

Risk: The HTML mailcap handler may pass untrusted MIME charset values through the shell.

Mitigation: Replace the mailcap handler with a reviewed version that does not pass untrusted MIME charset values through the shell before installing.

Risk: The skill can guide email composition in a client that is capable of sending messages.

Mitigation: Keep outgoing messages as drafts unless the user explicitly approves sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elmoyeldo/skills/neomutt-commander)
- [Skill homepage](https://github.com/LogicalSapien/agent-skills/tree/main/clawhub/neomutt-commander)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires neomutt and w3m; defaults outgoing email to draft creation unless sending is explicitly approved.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
