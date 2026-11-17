## Description:

Deploys the HXD Spring Boot service to a remote server by packaging the JAR, uploading it, backing up the previous version, restarting the service, and checking logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adtomato](https://clawhub.ai/user/adtomato)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy the HXD Spring Boot service to a configured remote host and report upload, backup, restart, and log-check status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make privileged remote production changes using root SSH access.

Mitigation: Use a dedicated deployment account and key, and require explicit confirmation that shows the target host, artifact path and checksum, backup name, and restart action before any remote mutation.

Risk: SSH commands disable strict host-key verification, weakening host identity checks.

Mitigation: Enable strict host-key verification and manage the target host key in known_hosts before deployment.

Risk: Broad deployment trigger phrases could cause an unintended deployment.

Mitigation: Remove broad automatic triggers or require a separate explicit approval immediately before upload, replacement, rollback, or restart.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adtomato/skills/hxd-deploy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status report with PowerShell and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports JAR upload status, timestamped backup name, service restart state, log-confirmed running status, and warnings or errors.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
