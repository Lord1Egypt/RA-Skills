## Description:

Factory edition of iaiops for inspecting and troubleshooting discrete-manufacturing systems across industrial protocols, with read-first workflows and MOC-gated writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Industrial automation and operations engineers use this skill to inspect PLCs, CNC equipment, gateways, and production data systems, then investigate downtime, alarms, OEE, and asset information. It favors read-first diagnostics; device writes require explicit change-control approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because three referenced paths were missing from the artifact.

Mitigation: Check that the referenced files are available and review the source and intended use before installing.

Risk: Some tools can write to industrial controllers or publish MQTT data, which can affect production systems.

Mitigation: Keep device writes disabled unless needed; use the documented dry-run, named MOC approval, double confirmation, and undo-value review, and never write without authorization.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zw008/skills/iaiops-factory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Configuration, Shell commands, Guidance]

**Output Format:** [Text and Markdown with operational analysis, configuration guidance, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-first diagnostic guidance; device-write operations are disabled by default and require change-control approval.]

## Skill Version(s):

0.34.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
