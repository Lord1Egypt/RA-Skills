## Description: <br>
Set up a local webhook server to receive Nansen smart alerts in real-time with HMAC signature verification and public tunneling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and crypto operations teams use this skill to create a local listener for Nansen smart alert webhook payloads, verify those payloads with HMAC signatures, and optionally forward verified alerts into OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The listener is reachable through a public tunnel, so unsigned requests can still reach the local machine. <br>
Mitigation: Use the required webhook secret and HMAC-SHA256 signature verification, keep the server bound to localhost, and stop the tunnel when finished. <br>
Risk: Tunnel URLs and webhook secrets can expose the endpoint if shared or logged. <br>
Mitigation: Treat the tunnel URL and webhook secret as sensitive, rotate the secret if exposed, and update Nansen alert configuration when a tunnel URL changes. <br>
Risk: Optional OpenClaw forwarding can trigger agent turns from verified alert payloads. <br>
Mitigation: Enable OpenClaw forwarding only when intentional and protect the gateway with the configured bearer token when auth is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-alerts-webhook-listener) <br>
- [Publisher profile](https://clawhub.ai/user/nansen-devops) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with inline bash commands and a Node.js server script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local webhook listener script, setup commands, and alert configuration guidance; optional OpenClaw forwarding is user-controlled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
