## Description: <br>
Secure outbound-only relay for remote OpenClaw control with no exposed ports, SSH, Telegram, or Discord dependency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-czar](https://clawhub.ai/user/jason-czar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, teams, and operators use PrivaClaw to remotely send prompts, trigger workflows, check node health, and restart an OpenClaw node over an outbound WebSocket relay without exposing local infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A compromised relay operator or leaked auth token could remotely run prompts, trigger workflows, read streamed responses or status, or restart the node. <br>
Mitigation: Install only with a trusted relay, protect and rotate AUTH_TOKEN, and use relay-side authorization, auditing, and workflow allowlists. <br>
Risk: Remote control of sensitive OpenClaw nodes can expose operational status and generated response content through the relay channel. <br>
Mitigation: Avoid sensitive nodes unless external controls are in place and confirm that prompt responses, workflow status, and heartbeat details are acceptable to transmit. <br>
Risk: Using an insecure relay URL can weaken the confidentiality of relay traffic. <br>
Mitigation: Prefer wss:// relay URLs and verify the configured relay endpoint before enabling the skill. <br>


## Reference(s): <br>
- [PrivaClaw ClawHub Page](https://clawhub.ai/jason-czar/privaclaw) <br>
- [Publisher Profile](https://clawhub.ai/user/jason-czar) <br>
- [Project Homepage](https://github.com/openclaw/privaclaw) <br>
- [Project Support](https://github.com/openclaw/privaclaw/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, status data, guidance] <br>
**Output Format:** [WebSocket JSON messages, streamed text responses, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RELAY_URL, NODE_ID, and AUTH_TOKEN; remote actions are limited to the declared relay capabilities.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
