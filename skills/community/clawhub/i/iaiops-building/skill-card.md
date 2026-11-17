## Description:

Supports building-automation work with read-first BACnet/IP, Modbus, IO-Link, MQTT, supervisory-controller, and half-hourly electricity analysis, plus approval-gated control commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Building-automation and facilities engineers use this skill to inspect HVAC, BMS, sensor, alarm, trend, and meter data and to guide troubleshooting. Device control is available only through the documented approval-gated workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One unresolved local reference leaves the security review incomplete.

Mitigation: Review and resolve the reference before installation.

Risk: BACnet, supervisory-controller, or MQTT write commands can change building equipment state.

Mitigation: Keep writes disabled by default and follow the documented dry-run and named dual-approval steps; SIS endpoints block writes and BAS life-safety points are refused.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zw008/skills/iaiops-building)
- [Publisher profile](https://clawhub.ai/user/zw008)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration, Shell commands]

**Output Format:** [Text and structured results, with Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-first results; device writes use documented approval controls.]

## Skill Version(s):

0.34.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
