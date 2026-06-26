## Description: <br>
Headless OpenClaw client for Ubuntu and Raspbian servers with heartbeat, auto-reconnect, auto-recovery, queue management, and hot model switching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris6970barbarian-hue](https://clawhub.ai/user/chris6970barbarian-hue) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run a headless OpenClaw gateway client on Ubuntu, Raspbian, Raspberry Pi, or cloud hosts. It supports persistent service operation with heartbeat reporting, reconnection, queue handling, recovery, and model switching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A long-running gateway-connected service can expose message contents and runtime telemetry to the configured gateway operator. <br>
Mitigation: Use only trusted gateways, prefer HTTPS for non-local gateways, and run the service only on hosts intended for persistent gateway connectivity. <br>
Risk: A broadly scoped API key could increase impact if the service host or gateway configuration is compromised. <br>
Mitigation: Use a dedicated low-privilege API key for this service and rotate it according to local credential policy. <br>
Risk: Enabling the systemd service makes the client persistent across restarts. <br>
Mitigation: Enable the service only when persistent background operation is desired and review the configured user, working directory, and gateway settings before deployment. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/chris6970barbarian-hue/glitch-kkclaw-server) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/chris6970barbarian-hue) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, JSON, and systemd configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied gateway URL and API key; intended for long-running headless service use.] <br>

## Skill Version(s): <br>
2026.2.17 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
