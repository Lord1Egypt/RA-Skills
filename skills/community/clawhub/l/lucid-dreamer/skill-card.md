## Description:

Lucid Dreamer is a nightly memory-maintenance skill that reviews an agent workspace's memory files and recent daily notes to find stale facts, unresolved tasks, contradictions, recurring issues, and durable updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run scheduled memory hygiene over local agent workspaces, producing review reports and optional high-confidence memory updates from daily notes and existing long-term memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended prompts may edit and commit long-term memory.

Mitigation: Review the prompts before scheduling, keep auto-apply and aggressive cleanup disabled unless explicitly accepted, and verify generated reports and git diffs regularly.

Risk: Workspace markdown may contain secrets or untrusted copied content that the review prompt reads.

Mitigation: Do not run the skill on notes containing plaintext secrets, credentials, or untrusted copied content; remove sensitive content before scheduling.

Risk: OpenClaw 2.0's built-in memory sweep can collide with Lucid if both run at 03:00.

Mitigation: Check scheduled automations first, then disable one memory sweep or separate their schedules so two unattended jobs do not rewrite the same memory file.

Risk: Memory suggestions can be plausible but wrong and may pollute long-term memory.

Mitigation: Require source citations, use high-confidence thresholds, review reports before accepting suggestions, and leave uncertain or judgment-based changes for manual approval.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/robbyczgw-cla/skills/lucid-dreamer)
- [README](README.md)
- [Architecture](ARCHITECTURE.md)
- [Auto-Apply Configuration](config/auto-apply.md)
- [OpenClaw ByteRover Context Engine PR](https://github.com/openclaw/openclaw/pull/50848)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown review reports, JSON state updates, configuration snippets, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads and writes local workspace memory files; trend detection prints Markdown to stdout.]

## Skill Version(s):

0.8.0 (source: SKILL.md frontmatter and CHANGELOG, released 2026-08-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
