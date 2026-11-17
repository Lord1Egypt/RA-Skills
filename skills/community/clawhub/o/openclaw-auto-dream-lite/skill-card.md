## Description:

Openclaw Auto Dream Lite consolidates OpenClaw daily memory logs into structured long-term memory and short status summaries through scheduled or manual dream cycles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myclaw-ai](https://clawhub.ai/user/myclaw-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to keep long-term agent memory current by consolidating daily logs into MEMORY.md and producing concise dream-cycle reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily autonomous execution can repeatedly read and rewrite long-term memory files without per-run user approval.

Mitigation: Enable the cron job only when unattended memory consolidation is desired, and document how to inspect, pause, or remove the scheduled task before installation.

Risk: Memory consolidation can introduce incorrect updates or unintended changes to MEMORY.md.

Mitigation: Review dream-log summaries after runs, keep the pre-dream backup, and use the documented rollback path if MEMORY.md appears corrupted.

Risk: The skill operates on personal or workspace memory content stored in MEMORY.md and memory/ logs.

Mitigation: Install only in workspaces where this scope is acceptable and review the memory files before enabling recurring execution.

## Reference(s):

- [Dream Prompt](references/dream-prompt.md)
- [Memory Template](references/memory-template.md)
- [ClawHub Skill Page](https://clawhub.ai/myclaw-ai/skills/openclaw-auto-dream-lite)
- [MyClaw.ai](https://myclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with shell commands and cron configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory file updates, dream-log entries, and concise user notifications.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
