## Description:

Perform comprehensive security audits, system updates, network and service status checks, and scheduled health monitoring for OpenClaw deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pettercc2024-create](https://clawhub.ai/user/pettercc2024-create)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system administrators use this skill to check OpenClaw host health, audit security posture, review service and dependency status, and configure recurring local health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cron command can create recurring checks and logs on a production host.

Mitigation: Review the configured schedule and log location before enabling recurring health checks.

Risk: Health and audit reports may expose system, network, service, or security posture details.

Mitigation: Store generated reports and logs in access-controlled locations and review them before sharing.

Risk: User-facing documentation and risk labels are primarily Chinese, which may affect review by teams that do not read Chinese.

Mitigation: Have an appropriate reviewer confirm the commands, risk labels, and remediation guidance before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pettercc2024-create/skills/openclaw-super-healthcheck)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces health reports with status summaries, issue lists, remediation advice, and risk scoring; optional cron setup writes recurring local logs.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
