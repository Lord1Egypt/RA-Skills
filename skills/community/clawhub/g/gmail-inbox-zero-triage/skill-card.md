## Description:

Gmail Inbox Zero Triage helps users process Gmail inbox messages with AI summaries and Telegram-button batch actions for archive, filter, unsubscribe, and view workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poisondminds](https://clawhub.ai/user/poisondminds)

### License/Terms of Use:

MIT

## Use Case:

External Gmail users and Clawdbot operators use this skill to triage Gmail inboxes quickly, review AI-generated summaries, and queue email actions before executing them in batch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Gmail read/modify access and can archive messages, create filters, and open unsubscribe links.

Mitigation: Use a dedicated Gmail account or the least-privilege OAuth grant available, and require explicit user review before executing unsubscribe, filter, or batch archive actions.

Risk: The setup guidance asks users to export GOG_KEYRING_PASSWORD, which could expose credentials through shell history or persistent shell profiles.

Mitigation: Avoid entering secrets directly in shell history or profile files; use a safer secret-management path supported by the runtime environment.

Risk: The artifact documentation references scripts that are not present in the provided artifact files.

Mitigation: Verify the installed .skill package contains the referenced scripts and inspect them before granting Gmail access.

Risk: The skill depends on the external gog CLI for Gmail access.

Mitigation: Pin or independently verify the gog CLI dependency before authorizing it against a Gmail account.

## Reference(s):

- [gog CLI](https://gogcli.sh)
- [Clawdbot documentation](https://docs.clawd.bot)
- [SETUP.md](SETUP.md)
- [OVERVIEW.md](OVERVIEW.md)
- [ClawHub skill page](https://clawhub.ai/poisondminds/skills/gmail-inbox-zero-triage)
- [Publisher profile](https://clawhub.ai/user/poisondminds)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and interactive email action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces concise email summaries and queued Gmail action recommendations for user review before batch execution.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact documentation references 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
