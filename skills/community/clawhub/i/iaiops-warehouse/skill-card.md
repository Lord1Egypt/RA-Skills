## Description:

Supports warehouse and intralogistics operations with industrial-protocol monitoring, predictive maintenance, downtime triage, throughput analysis, and alarm review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and industrial operations engineers use this skill to inspect warehouse PLC, drive, WMS/WCS, and fleet data, then investigate downtime, equipment health, alarms, and throughput. It also guides carefully controlled maintenance or configuration actions where supported.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may invoke the skill in conversations unrelated to warehouse operations.

Mitigation: Use it for warehouse and intralogistics tasks, and check that the request is within that context before applying its guidance.

Risk: Some supported tools can write to production control systems or publish MQTT messages.

Mitigation: Keep use read-first; for writes, follow the documented MOC process with dry-run review, named approval, before-value undo, and double confirmation.

## Reference(s):

- [Industrial-AIOps Warehouse on ClawHub](https://clawhub.ai/zw008/skills/iaiops-warehouse)

## Skill Output:

**Output Type(s):** [Analysis, Text, Configuration, Shell commands, Files]

**Output Format:** [Diagnostic summaries, operational guidance, configuration drafts, and structured reports such as Markdown, JSON, or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings depend on available site data; unverified mappings and unknown device details should remain explicit.]

## Skill Version(s):

0.34.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
