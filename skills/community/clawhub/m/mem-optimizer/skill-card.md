## Description:

Mem Optimizer scans workspace memory files, estimates token usage, summarizes long entries, reports memory statistics, and can run scheduled memory maintenance across active agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doony15](https://clawhub.ai/user/doony15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to preview or perform memory-file compression, inspect token usage, and generate daily memory maintenance summaries for single-agent or multi-agent OpenClaw workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite memory files when dry-run mode is disabled.

Mitigation: Keep dry-run mode enabled until reviewed results are acceptable, and maintain backups before allowing file writes.

Risk: Scheduled global execution can run memory maintenance without a direct user prompt.

Mitigation: Install only when daily scheduled memory maintenance is desired, and disable or remove the cron entry if automatic execution is not approved.

Risk: Multi-agent mode can inspect and modify memory across agent workspaces.

Mitigation: Use multi-agent mode only for authorized workspaces and confirm every target agent is in scope before disabling dry-run mode.

Risk: Daily reports collect host and agent status.

Mitigation: Review the report destination and limit deployment to environments where host and agent status collection is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/doony15/skills/mem-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON tool results and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes token counts, processed-file details, dry-run status, multi-agent summaries, and daily report data.]

## Skill Version(s):

1.2.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
