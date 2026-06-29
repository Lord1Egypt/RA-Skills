## Description: <br>
Bridge IoT devices to the cloud via aitun tunnel. Expose local MQTT brokers, device dashboards, or HTTP APIs so remote devices and services can connect, report data, and receive commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctz168](https://clawhub.ai/user/ctz168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to expose local IoT services, dashboards, MQTT brokers, or HTTP APIs through an aitun tunnel for remote device access, testing, and data reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose local IoT services such as Home Assistant, Node-RED, Grafana, MQTT, or device-control APIs to the internet. <br>
Mitigation: Require strong authentication on exposed services, review who can reach the tunnel URL, and avoid exposing device-control APIs unless the access model is understood. <br>
Risk: The artifact includes one-line remote installer commands for Linux, macOS, and Windows. <br>
Mitigation: Prefer the pip or uv install path, or independently verify remote installer scripts before executing them. <br>


## Reference(s): <br>
- [AiTun homepage](https://aitun.cc) <br>
- [ClawHub skill page](https://clawhub.ai/ctz168/skills/iot-bridge) <br>
- [ClawHub listing from OpenClaw metadata](https://clawhub.ai/ctz168/iot-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes install commands, tunnel commands, endpoint-sharing guidance, cleanup commands, and CLI flag notes.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
