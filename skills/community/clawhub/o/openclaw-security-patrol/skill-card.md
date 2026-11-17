## Description:

Runs an OpenClaw security patrol that performs local system and Skill inventory checks by default, with an optional user-confirmed mode that submits audit summaries to Changeway threat intelligence endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zsyjx0115](https://clawhub.ai/user/zsyjx0115)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to run local security audits, review saved audit reports, and optionally request a remote threat intelligence score after explicit consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs broad local inspection and reads sensitive host, system log, and Skill inventory data.

Mitigation: Install only when that inspection scope is acceptable, review the local reports it creates, and prefer the default local mode for privacy-sensitive environments.

Risk: The optional push mode can send host identifiers, Skill inventory, and audit summaries to auth.ctct.cn.

Mitigation: Use push mode only after explicit informed consent and only when the publisher-operated endpoint is trusted.

Risk: Recurring scans through OpenClaw cron can repeatedly inspect the machine and create stored reports.

Mitigation: Enable cron only when recurring scans are desired, keep scheduled runs in local mode, and avoid adding push behavior to scheduled jobs.

Risk: Security evidence notes a persistent agent_id behavior even during offline scans.

Mitigation: Review local state files before deployment and document retention expectations for any persistent device identifier.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zsyjx0115/skills/openclaw-security-patrol)
- [Cron setup guide](references/cron-setup.md)
- [Changeway audit data endpoint](https://auth.ctct.cn:10020/changeway-open/api/pushAuditData)
- [Changeway Skill assessment endpoint](https://auth.ctct.cn:10020/changeway-open/api/skills/assessment)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and concise audit summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local text and JSON audit reports under the OpenClaw state directory.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
