## Description:

Bridge IoT devices to the cloud via aitun tunnel. Expose local MQTT brokers, device dashboards, or HTTP APIs so remote devices and services can connect, report data, and receive commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctz168](https://clawhub.ai/user/ctz168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and IoT engineers use this skill to expose local MQTT brokers, device dashboards, HTTP APIs, and other IoT services through an aitun tunnel for remote access, testing, and cloud integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to expose local IoT dashboards, MQTT brokers, and device APIs to the internet.

Mitigation: Use the skill only when authentication, TLS, access controls, and network segmentation are already in place.

Risk: The artifact includes one-line remote script installers for Linux, macOS, and Windows.

Mitigation: Prefer a pinned and verified aitun package installed in an isolated environment before running tunnel commands.

Risk: The server security verdict is suspicious because the tunneling workflow lacks sufficient safeguards for exposed IoT services.

Mitigation: Review the skill carefully before installation and avoid exposing sensitive services unless the operational risk has been accepted.

## Reference(s):

- [AiTun homepage](https://aitun.cc)
- [ClawHub skill page](https://clawhub.ai/ctz168/skills/iot-bridge)
- [ClawHub package link from metadata](https://clawhub.ai/ctz168/iot-bridge)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes install commands, tunnel setup commands, endpoint-sharing guidance, CLI flags, and cleanup steps.]

## Skill Version(s):

1.0.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
