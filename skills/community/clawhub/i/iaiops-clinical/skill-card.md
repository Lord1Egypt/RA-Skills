## Description:

Provides clinical-facility monitoring and analysis workflows for BACnet, Modbus, and OPC UA systems, including isolation-room pressure, medical-gas, and operating-room environment checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Hospital and healthcare facility engineers use the skill to inspect building-management and plant data, review isolation-room pressure and medical-gas readings, and analyze alarms, trends, and downtime. Its analyses support facility workflows and should be checked against site procedures and primary safety monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised read-only posture conflicts with a BACnet device-write tool, which could allow unintended changes to clinical facility equipment.

Mitigation: Review permissions and confirm device writes are disabled or separately controlled before clinical facility use.

Risk: Clinical safety checks analyze supplied readings and may not reflect current conditions or replace site alarm and infection-control procedures.

Mitigation: Validate readings and findings against facility monitoring, alarm panels, and established clinical engineering procedures.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zw008/skills/iaiops-clinical)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration, Files]

**Output Format:** [Text and Markdown reports, structured tool results, and configuration drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include protocol readings, safety-check findings, alarm and trend summaries, and exportable reports.]

## Skill Version(s):

0.34.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
