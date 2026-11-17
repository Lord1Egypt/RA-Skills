## Description:

Email inbox triage for AI agents that scans unread messages, categorizes urgency, drafts replies, surfaces urgent items, and identifies archive candidates for Gmail and IMAP workflows.

This skill is for research and development only.

## Publisher:

[clawdssen](https://clawhub.ai/user/clawdssen)

### License/Terms of Use:

CC-BY-NC-4.0

## Use Case:

Employees, external users, and operators use this skill to turn unread email into a concise triage report with urgency categories, summaries, and recommended next actions. It can also guide configuration for reply drafting, scheduled checks, multi-account handling, and optional archive workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive inbox subjects and message bodies.

Mitigation: Use read-only, unread-only, and headers-only access where possible, and avoid storing full email content.

Risk: Optional archive workflows could hide important messages if triage rules are wrong.

Mitigation: Require explicit confirmation before live archiving, keep an archive label or folder, and run a dry-run review period before enabling automated moves.

Risk: Optional reply drafting or sending workflows could send inappropriate or incomplete responses.

Mitigation: Keep reply sending disabled by default and require human approval for every draft before any message is sent.

Risk: External notifications and escalation chains may disclose sensitive email metadata.

Mitigation: Disable Telegram, backup-contact escalation, and similar notification paths unless destinations are trusted and the user explicitly enables them.

Risk: Persistent sender profiling can reveal private communication patterns.

Mitigation: Disable memory profiling unless there is a clear need, keep profiles minimal, and review stored sender data regularly.

## Reference(s):

- [Inbox Triage Advanced Patterns](references/advanced-patterns.md)
- [Inbox Triage on ClawHub](https://clawhub.ai/clawdssen/skills/inbox-triage)
- [clawdssen Publisher Profile](https://clawhub.ai/user/clawdssen)
- [The Agent Ledger](https://www.theagentledger.com)
- [gmailctl](https://github.com/mbrt/gmailctl)
- [himalaya](https://github.com/pimalaya/himalaya)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and configuration guidance with optional inline shell commands and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-readable triage summaries, suggested actions, optional reply drafts, and setup or workflow guidance; does not require persistent output files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
