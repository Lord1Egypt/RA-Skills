## Description:

Read, search, and download email over IMAP from the command line using the `myl` CLI client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aggrrrh](https://clawhub.ai/user/aggrrrh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to let an agent check inboxes, search mailbox contents, read selected messages, and save attachments through a configured read-only IMAP CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured mailbox becomes accessible to the agent while the skill is enabled.

Mitigation: Install only when that access is acceptable, use a narrowly scoped app password, and prefer short-lived environment injection or OpenClaw SecretRef for credentials.

Risk: Mailbox credentials can be exposed through unsafe argument forwarding or process inspection while the IMAP client runs.

Mitigation: Avoid shared or monitored machines and do not allow user-supplied connection or authentication flags until the wrapper validates or rejects them.

Risk: The skill depends on the third-party `myl` package for mailbox access.

Mitigation: Pin or review the `myl` dependency before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aggrrrh/skills/imap-client)
- [Authentication and connection](references/authentication.md)
- [Installation](references/installation.md)
- [Operations](references/operations.md)
- [Recipes](references/recipes.md)
- [Troubleshooting](references/troubleshooting.md)
- [myl IMAP CLI](https://github.com/pschmitt/myl)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown summaries with inline shell commands, configuration snippets, and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local .eml, .html, or attachment files when the user asks to save message content.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
