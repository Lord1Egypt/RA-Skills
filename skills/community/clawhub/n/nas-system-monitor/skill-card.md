## Description:

Monitors local NAS disk usage, memory, and CPU temperature, printing threshold alerts for operators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sasamittrrr](https://clawhub.ai/user/sasamittrrr)

### License/Terms of Use:


## Use Case:

Developers and NAS operators use this skill to run a local foreground monitor for Linux-based NAS health checks and review threshold alerts for disk, memory, and CPU temperature. It is not evidence-supported as a complete unattended remote alerting solution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises Feishu, Discord, and Telegram notifications, but the artifact does not implement remote notification delivery.

Mitigation: Treat the skill as local foreground monitoring unless notification delivery is implemented and tested before unattended use.

Risk: The release advertises network, Docker container, and critical process monitoring beyond the checks implemented in the artifact.

Mitigation: Validate required checks against the shipped code and add missing monitoring coverage before relying on the skill for NAS operations.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sasamittrrr/skills/nas-system-monitor)
- [Publisher profile](https://clawhub.ai/user/sasamittrrr)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and terminal alert text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs as a foreground local process; remote notification delivery is not implemented in the artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
