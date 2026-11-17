## Description:

Safe OpenClaw config change workflow with backup, minimal edits, validation, health checks, and rollback. Single-instance first; secondary instance optional.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1987566643](https://clawhub.ai/user/1987566643)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to make OpenClaw configuration changes through a backup-first workflow with validation, health checks, and rollback steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The safety script changes OpenClaw configuration and service state, and automatic rollback may not cover every failure path.

Mitigation: Review the shell script before production use, keep known-good backups, and verify OpenClaw status and gateway health after each change.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown with bash command examples and script-file workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
