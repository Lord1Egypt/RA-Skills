## Description:

Provides read-first tools for analyzing solar PV and wind assets, plant telemetry, equipment health, alarms, downtime, and half-hourly electricity data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Renewable-energy and industrial-operations engineers use this skill to inspect solar and wind equipment, analyze SCADA and telemetry, investigate equipment health, downtime and alarms, and profile half-hourly electricity meter data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation terms may engage the skill in unrelated conversations.

Mitigation: Use it for renewable-energy and related industrial AIOps work, and review its scope before acting on its guidance.

Risk: The optional MQTT publish operation can write to site telemetry systems.

Mitigation: Keep publishing in dry-run unless the required named management-of-change approval and double confirmation are in place; SIS endpoints reject device writes.

## Reference(s):

- [Industrial-AIOps Renewables on ClawHub](https://clawhub.ai/zw008/skills/iaiops-renewables)
- [Publisher profile: zw008](https://clawhub.ai/user/zw008)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration, Shell commands, Reports]

**Output Format:** [Structured text, Markdown reports, and configuration drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-first workflows; optional MQTT publishing is management-of-change gated.]

## Skill Version(s):

0.34.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
