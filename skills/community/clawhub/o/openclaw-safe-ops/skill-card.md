## Description:

Guards high-risk OpenClaw operations with preflight backups, post-change health checks, and rollback guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhrxy](https://clawhub.ai/user/dhrxy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill before high-risk OpenClaw gateway, configuration, plugin, or openclaw.json changes to capture backups, run health checks, and report rollback status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suggested ./scripts/openclaw-safe.sh wrapper is not bundled with the artifact.

Mitigation: Do not run the wrapper unless its exact script and location have been independently verified.

Risk: Rollback commands may restore a different file than the backup created immediately before the change.

Mitigation: Use the specific timestamped backup path created during preflight and confirm the copy succeeds before restarting OpenClaw.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and operational status notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the command executed, backup path, health check results, and whether rollback was needed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
