## Description:

Checks the functional integrity and operational status of a local mem0 memory system when asked about mem0 status, functionality, or completeness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chircken891](https://clawhub.ai/user/chircken891)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and local administrators use this skill to run and summarize health checks for semantic search, memory counts, cron tasks, and Chroma storage in a local mem0 setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A health check may expose full local memory contents.

Mitigation: Use only in a trusted local admin context, ask before running commands, and return sanitized health, count, and connectivity results instead of raw memory contents.

Risk: The workflow runs local diagnostics against user-specific Windows paths and mem0 resources.

Mitigation: Confirm the target environment and paths before execution, and avoid running diagnostics on shared or untrusted machines.

## Reference(s):

- [Mem0 Status Check ClawHub Page](https://clawhub.ai/chircken891/skills/mem0-status-check)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown status report with PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include counts, health statuses, missing-feature notes, and improvement suggestions for a local mem0 installation.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
