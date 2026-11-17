## Description:

Combined network and gateway status with VPN info, IP location, and system health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[space-cadet](https://clawhub.ai/user/space-cadet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect current network, VPN, Tailscale, gateway, and system status from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects and displays detailed network status, including private addresses, VPN/Tailscale details, routes, uptime, and gateway status.

Mitigation: Use it only in trusted sessions and avoid sharing raw output when network details are sensitive.

Risk: The public-IP geolocation check contacts ipinfo.io, which can see the connection's public source IP and request metadata.

Mitigation: Run the lookup only when that external request is acceptable for the environment.

## Reference(s):

- [ipinfo.io public IP JSON endpoint](https://ipinfo.io/json)
- [ClawHub Netstatus skill page](https://clawhub.ai/space-cadet/skills/netstatus)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style network status summary with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local network addresses, VPN and Tailscale details, public IP geolocation, gateway status, and uptime.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
