## Description: <br>
Use the MeshMonitor REST API to inspect Meshtastic mesh state, nodes, channels, telemetry, messages, traceroutes, packets, solar data, and network-wide stats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dadud](https://clawhub.ai/user/dadud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to query authenticated MeshMonitor instances, inspect mesh health, build node and traffic reports, and create reusable API integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper includes commands that can send live mesh messages or make arbitrary authenticated API requests. <br>
Mitigation: Use a read-only or low-privilege token for reporting, and require human approval before running send-message or raw non-GET requests. <br>
Risk: The skill requires an API token for a MeshMonitor instance. <br>
Mitigation: Provide tokens only at runtime, test authentication with a lightweight request first, and rotate or revoke tokens that fail or may have been exposed. <br>


## Reference(s): <br>
- [MeshMonitor API Notes](references/api-notes.md) <br>
- [ClawHub release page](https://clawhub.ai/dadud/meshmonitor-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authenticated API call guidance, generated helper commands, structured mesh health summaries, node inventories, message and telemetry digests, troubleshooting notes, and reusable integration code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
