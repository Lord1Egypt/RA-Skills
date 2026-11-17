## Description:

Headless OpenClaw client for Ubuntu and Raspbian servers with heartbeat, auto-reconnect, recovery, queue management, and hot model switching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris6970barbarian-hue](https://clawhub.ai/user/chris6970barbarian-hue)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run a headless KKClaw/OpenClaw client on Ubuntu, Raspbian, Raspberry Pi, or cloud hosts with resilient gateway connectivity and model-management controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The client can send API keys, messages, and telemetry over unencrypted HTTP.

Mitigation: Use HTTPS for any non-local gateway and protect or avoid plaintext API keys in configuration files.

Risk: The artifact documents persistent system service operation.

Mitigation: Run systemd deployments under a dedicated least-privilege account, harden the unit, and document how to stop, disable, and remove the service.

## Reference(s):

- [Kkclaw Server ClawHub listing](https://clawhub.ai/chris6970barbarian-hue/skills/glitch-kkclaw-server)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash, JSON, JavaScript, and systemd configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational setup guidance for a Node.js headless client and gateway configuration.]

## Skill Version(s):

2026.2.17 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
