## Description:

OpenClaw Watchdog Pro helps agents guide users through cross-platform OpenClaw configuration backup, gateway monitoring, automatic rollback, and gateway error-pattern checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doradx](https://clawhub.ai/user/doradx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to configure a persistent watchdog that backs up OpenClaw configuration, checks gateway health, restores the latest valid backup, and analyzes gateway log error patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can configure a persistent long-running OpenClaw watchdog service.

Mitigation: Install only when persistent monitoring is intended, review the installer before use, and maintain a clear uninstall or disable procedure.

Risk: The watchdog may run with elevated privileges through system services or scheduled tasks.

Mitigation: Prefer a least-privileged user service and avoid administrator or root execution unless operationally required.

Risk: Automatic repair or rollback can change OpenClaw configuration without enough user control.

Mitigation: Consider disabling automatic repair or rollback, and review backups and recovery actions before relying on unattended remediation.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and operational procedures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are operational guidance for local OpenClaw configuration, service setup, monitoring, backup, recovery, and troubleshooting.]

## Skill Version(s):

2.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
