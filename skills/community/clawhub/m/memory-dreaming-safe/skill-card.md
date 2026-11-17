## Description:

Memory Dreaming (Safe Edition) helps OpenClaw agents consolidate daily logs, learnings, session signals, and plan notes into long-term memory and optional Obsidian notes with documented confirmation gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deathrowsushy](https://clawhub.ai/user/deathrowsushy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review and consolidate noisy agent memory, extract durable learnings from logs and transcripts, and optionally sync structured knowledge into an Obsidian or markdown knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled execution can silently read broad history and modify long-term memory or Obsidian notes despite the documentation's confirmation-gate posture.

Mitigation: Review carefully before installing and do not enable the cron job until the scheduled prompt is changed to produce a reviewable proposal instead of writing automatically.

Risk: Transcript scanning and broad workspace plan scans can expose sensitive or unrelated workspace information.

Mitigation: Use a dedicated, non-sensitive memory workspace and disable transcript scanning and broad workspace plan scans unless they are explicitly needed.

Risk: Obsidian sync may copy consolidated memory into a separate knowledge base.

Mitigation: Keep Obsidian sync disabled unless the target vault is private and appropriate for the information being consolidated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deathrowsushy/skills/memory-dreaming-safe)
- [Architecture - Memory Dreaming](references/architecture.md)
- [Dream Prompt](references/dream-prompt.md)
- [Obsidian Sync - How It Works](references/obsidian-sync.md)
- [Default dreaming configuration](assets/dreaming-config.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, proposed diffs, shell commands, and configuration JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce proposed memory updates, dreaming logs, and Obsidian markdown notes depending on configuration and user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
