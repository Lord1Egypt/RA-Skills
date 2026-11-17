## Description:

Check that every service is monitored and alerts really arrive: gaps between service list and monitors, dead man's switches for timed jobs and backups, approved alert tests with evidence, monitoring tool versions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[holgergruenhagen](https://clawhub.ai/user/holgergruenhagen)

### License/Terms of Use:

MIT-0

## Use Case:

Service owners and operators use this skill to compare named services, hosts, jobs, and backups with their monitors, identify coverage gaps, and assess alert delivery and tool versions. It produces a scoped report and approval-ready proposals while leaving monitoring changes and alert tests to the owner's approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An end-to-end alert test can send real messages and change monitor state or uptime figures.

Mitigation: Obtain approval for each test after showing its route, expected message, side effects, and who will confirm delivery.

Risk: Host and monitoring discovery can reveal operational details, while monitoring credentials and alert destinations may be sensitive.

Mitigation: Stay within the owner's named scope, use read-only access where possible, and omit secrets and personal recipient details from reports.

## Reference(s):

- [Uptime Kuma latest release API](https://api.github.com/repos/louislam/uptime-kuma/releases/latest)
- [healthchecks.io checks API](https://healthchecks.io/api/v3/checks/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with a coverage matrix, gap list, approval-ready proposals, alert-test evidence, and version notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scope-specific; reports avoid secrets and personal recipient details.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
