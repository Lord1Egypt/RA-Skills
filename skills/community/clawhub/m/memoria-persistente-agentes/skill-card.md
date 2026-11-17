## Description:

Persistent memory system for AI agents inspired by Letta/MemGPT, using Core, Archival, and Recall layers so agents can remember user preferences, context, decisions, and prior sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renateparma](https://clawhub.ai/user/renateparma)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to add persistent, file-backed memory to OpenClaw, Claude Code, Codex, or generic agents. It supports session-start context loading, user-requested memory updates, archival notes, and periodic memory maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable local memory can retain sensitive personal context longer than a single session.

Mitigation: Do not store secrets, medication details, or other sensitive personal data in memory files; review memory contents before enabling broad reuse.

Risk: Session synchronization can index all sessions visible to the configured OpenClaw account.

Mitigation: Run session-sync.py only when that scope is intended and approved, and limit access to the account and workspace being indexed.

Risk: Automated heartbeat or cron maintenance can update memory without direct per-entry review.

Mitigation: Avoid enabling the cron job until review and approval controls are in place.

## Reference(s):

- [Letta Memory Integration Guide](references/integration.md)
- [ClawHub release page](https://clawhub.ai/renateparma/skills/memoria-persistente-agentes)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts may create or update local memory Markdown files and JSON session indexes when run.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
