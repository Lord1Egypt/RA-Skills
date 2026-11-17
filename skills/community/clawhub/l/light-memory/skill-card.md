## Description:

A lightweight, prompt-driven three-layer memory system for long-term context retention in OpenClaw agents using Markdown files and scheduled OpenClaw cron tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason99666](https://clawhub.ai/user/jason99666)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent developers use this skill to install and operate a file-backed L1/L2/L3 memory workflow that extracts marked decisions, insights, tasks, and summaries from session logs into auditable Markdown memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring background jobs read OpenClaw session logs and retain summaries in long-term Markdown memory files.

Mitigation: Require explicit opt-in for each cron task, document what session files are scanned, and add sensitive-data redaction before enabling scheduled extraction.

Risk: The session cleanup workflow can delete session files based on filename and size rules.

Mitigation: Run cleanup in dry-run or review mode first, show the exact files selected for deletion, and keep backups or disable GC until the retention policy is accepted.

Risk: Automatic memory extraction can preserve sensitive or stale information beyond the original conversation.

Mitigation: Provide clear pause and uninstall steps, periodically review memory files, and avoid storing credentials or confidential material in marked memory content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jason99666/skills/light-memory)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Architecture reference](artifact/references/architecture.md)
- [CAR format reference](artifact/references/car-format.md)
- [Troubleshooting reference](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command snippets and generated Markdown memory files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local memory files, prompt templates, OpenClaw cron entries, backups, and status reports.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
