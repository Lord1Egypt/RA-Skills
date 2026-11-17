## Description:

Lobster Doctor helps OpenClaw users diagnose workspace health, preview cleanup actions, slim skill descriptions, archive memory, inspect session health, and audit cron jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masongmx](https://clawhub.ai/user/masongmx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw workspace users use this skill to review workspace health, identify stale or duplicate files and skills, preview cleanup actions, archive old memory entries, and reduce skill description token overhead.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace cleanup and skill slimming commands can move files or rewrite installed skill metadata.

Mitigation: Start with read-only report or dry-run modes, inspect previews and backups, and run cleanup or apply modes only with explicit intent.

Risk: Generated reports can include session identifiers, agent names, skill inventory, cron details, and messaging-channel targets.

Mitigation: Treat reports as sensitive local workspace data and avoid sharing them outside trusted review channels.

Risk: The security review marks the release suspicious because broad maintenance commands have weaker controls than the documentation promises.

Mitigation: Review the skill before installing and keep initial use limited to read-only or report modes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/masongmx/skills/lobster-doctor-skill-slim)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text reports with optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local reports or backups when the user runs cleanup, archive, or weekly-report workflows.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
