## Description: <br>
Set up and troubleshoot a hybrid OpenClaw architecture where a cloud VPS runs the gateway and a local machine acts as a node for hardware, browser, local model, and macOS capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkfaris94](https://clawhub.ai/user/jkfaris94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect a local OpenClaw node to a VPS-hosted gateway, configure Tailscale networking, set up service auto-start, route exec commands, and troubleshoot pairing or connectivity failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gateway exposure could make the OpenClaw gateway reachable beyond the intended local setup. <br>
Mitigation: Restrict port 18789 to Tailscale or trusted IPs, prefer wss:// when possible, and use token auth with rate limiting. <br>
Risk: Remote exec routing can let agents run commands on the local node. <br>
Mitigation: Review node command approvals carefully and avoid broad allowlist entries such as /bin/bash unless that access is intentional. <br>
Risk: Gateway tokens can grant access if leaked through shell history, service files, or logs. <br>
Mitigation: Protect the gateway token, keep it in the node service environment only where needed, and rotate it if exposed. <br>
Risk: Auto-start can keep the node continuously available for remote work even when the user is not actively operating it. <br>
Mitigation: Enable LaunchAgent or systemd auto-start only when continuous node availability is intended. <br>


## Reference(s): <br>
- [Hybrid Gateway ClawHub page](https://clawhub.ai/jkfaris94/hybrid-gateway) <br>
- [Publisher profile](https://clawhub.ai/user/jkfaris94) <br>
- [OpenClaw node host docs](https://docs.openclaw.ai/nodes/) <br>
- [Tailscale download](https://tailscale.com/download) <br>
- [Tailscale Serve](https://tailscale.com/kb/1242/tailscale-serve) <br>
- [GitHub SSH key guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; includes environment variable names and operational troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
