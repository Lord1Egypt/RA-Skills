## Description:

Control NordVPN on Linux via the `nordvpn` CLI (connect/disconnect, choose country/city/group, read status, tweak settings, manage allowlist). Use for automation that needs region routing or temporary VPN tunneling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maciekish](https://clawhub.ai/user/maciekish)

### License/Terms of Use:


## Use Case:

Developers and automation operators use this skill to manage local Linux NordVPN CLI connections, inspect VPN status, select routing locations, and adjust related settings from agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: VPN connection, disconnection, kill switch, protocol, autoconnect, and allowlist changes can disrupt active network sessions, especially over SSH or on shared systems.

Mitigation: Run disruptive NordVPN actions only with explicit user intent and verify status after changes.

Risk: NordVPN account or status output may contain sensitive operational details if copied into logs or shared transcripts.

Mitigation: Avoid exposing raw account and status output beyond what is needed to complete the task.

## Reference(s):

- [NordVPN](https://nordvpn.com/)
- [ClawHub NordVPN Skill](https://clawhub.ai/maciekish/skills/nordvpn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and concise status or troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command sequences for local VPN connection, disconnection, status checks, settings, and allowlist changes.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
