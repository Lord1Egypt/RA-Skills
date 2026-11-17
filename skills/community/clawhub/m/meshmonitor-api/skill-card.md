## Description:

Use the MeshMonitor REST API to inspect Meshtastic mesh state, nodes, channels, telemetry, messages, traceroutes, packets, solar data, and network-wide stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dadud](https://clawhub.ai/user/dadud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query MeshMonitor instances, inspect mesh health and history, generate node and traffic reports, and build reusable MeshMonitor API automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A MeshMonitor bearer token can grant the agent the same read and write powers as the user.

Mitigation: Use least-privilege or read-only tokens where available, keep tokens out of shell history, and revoke or rotate tokens after use.

Risk: The skill can send live mesh messages through MeshMonitor.

Mitigation: Require explicit human approval before using send-message or any non-GET raw API request.

Risk: Mesh data and credentials may be exposed if sent to an untrusted or plaintext endpoint.

Mitigation: Prefer HTTPS-only MeshMonitor base URLs and confirm the target instance before making authenticated requests.

## Reference(s):

- [MeshMonitor API Notes](references/api-notes.md)
- [MeshMonitor API skill release](https://clawhub.ai/dadud/skills/meshmonitor-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance, JSON API responses, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call live MeshMonitor endpoints with a user-provided base URL and bearer token.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
