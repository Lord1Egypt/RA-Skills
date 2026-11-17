## Description:

Organize, deduplicate, summarize, and compress OpenClaw or Clawd memory files into concise, durable workspace memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1217047020](https://clawhub.ai/user/1217047020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw or Clawd users use this skill to inspect, back up, deduplicate, summarize, and maintain workspace memory files without losing durable preferences or environment facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory cleanup can remove useful context or compress details too aggressively.

Mitigation: Review the proposed MEMORY.md and daily-note edits before approving changes.

Risk: Rewriting memory files can make accidental data loss harder to recover from.

Mitigation: Create and retain the bundled backup before any rewrite.

Risk: Private or sensitive strings may exist in raw memory notes.

Mitigation: Prefer omitting sensitive data from long-term memory unless it is explicitly needed.

## Reference(s):

- [OpenClaw Memory Curator on ClawHub](https://clawhub.ai/1217047020/skills/openclaw-memory-curator)
- [README](artifact/README.md)
- [CHANGELOG](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON reports and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports backup location, MEMORY.md changes, before and after memory totals, and intentionally kept or dropped items.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, and changelog released 2026-03-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
