## Description:

Autonomous memory consolidation for OpenClaw agents that periodically gathers signal from daily logs, session transcripts, learnings, and plans, then updates long-term memory and optionally syncs structured knowledge to Obsidian.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oryanmoshe](https://clawhub.ai/user/oryanmoshe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to schedule or manually run memory maintenance that consolidates agent notes, corrections, decisions, and plans into durable memory and optional Obsidian notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended memory consolidation can read transcripts, daily logs, task plans, and vault content that may contain credentials, private URLs, personal information, or sensitive project data.

Mitigation: Review transcript and workspace scope before enabling cron, keep Obsidian sync disabled until a dedicated vault path is configured, and add redaction or review steps for sensitive data.

Risk: Consolidated memory or Obsidian notes can persist incorrect, stale, or contradictory facts if the source material is noisy.

Mitigation: Review memory and dreaming-log changes after early runs, use manual dream cycles before unattended scheduling, and correct durable memory entries promptly.

Risk: Periodic cron execution gives an isolated agent recurring access to broad memory and plan data.

Mitigation: Use the built-in time gate, restrict workspace and vault paths where possible, and avoid unattended cron use until access scope and memory deletion behavior are acceptable.

## Reference(s):

- [Architecture](references/architecture.md)
- [Dream Prompt](references/dream-prompt.md)
- [Obsidian Sync](references/obsidian-sync.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON configuration, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update MEMORY.md, memory/dreaming-log.md, learning status files, and opt-in Obsidian vault notes.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
