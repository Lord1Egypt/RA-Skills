## Description: <br>
Connects OpenClaw to the Clawhome chat platform so an agent can send and receive messages for automatic replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shengguo](https://clawhub.ai/user/shengguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install the Clawhome channel plugin, restart the OpenClaw gateway, and configure Clawhome channel credentials for messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer invokes OpenClaw plugin installation or update commands and restarts the OpenClaw gateway. <br>
Mitigation: Run it only in an environment where you trust the npm package, the OpenClaw plugin, and the Clawhome service, and review the printed fallback commands before manual execution. <br>
Risk: Clawhome channel secrets are configured through shell commands and could be exposed in shared terminals, shell history, or screenshots. <br>
Mitigation: Treat the channel secret like a password, avoid exposing it in shared contexts, and rotate it if disclosure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shengguo/openclaw-clawhome-cli) <br>
- [OpenClaw installation documentation](https://docs.openclaw.ai/install) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MQTT topic examples, heartbeat and message payload examples, and configuration key names for Clawhome.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
