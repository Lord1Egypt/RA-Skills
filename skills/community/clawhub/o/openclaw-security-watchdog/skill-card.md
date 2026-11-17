## Description:

OpenClaw security-watchdog runs local OpenClaw and system security checks, produces concise audit results, and can optionally submit audit summaries and installed-skill inventory to Changeway for threat-intelligence scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ylardablez](https://clawhub.ai/user/ylardablez)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users run this skill to inspect local system posture, OpenClaw configuration, cron jobs, logs, installed skills, and related security signals. It is intended for manual security audits, optional scheduled local reporting, and user-confirmed Changeway threat-intelligence checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local and Agent-state inspection can expose sensitive local context in audit artifacts.

Mitigation: Run the skill only when a comprehensive OpenClaw security audit is intended, prefer normal user privileges, and review locally saved reports before sharing them.

Risk: Push mode sends stable device identifiers, installed skill inventory, and audit summaries to a third-party Changeway endpoint.

Mitigation: Use local mode by default and enable push mode only for a single manual run after informed consent.

Risk: A scheduled job with push mode would repeatedly upload device and skill inventory data.

Mitigation: Review OpenClaw cron configuration before enabling it and keep --push out of scheduled jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ylardablez/skills/openclaw-security-watchdog)
- [Cron setup guide](references/cron-setup.md)
- [Changeway audit upload endpoint](https://auth.ctct.cn:10020/changeway-open/api/pushAuditData)
- [Changeway skill assessment endpoint](https://auth.ctct.cn:10020/changeway-open/api/skills/assessment)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown and text summaries with shell commands for running audits or configuring OpenClaw cron jobs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local text and JSON reports under the user's OpenClaw state directory; optional push mode sends summaries and installed-skill inventory after user confirmation.]

## Skill Version(s):

1.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
