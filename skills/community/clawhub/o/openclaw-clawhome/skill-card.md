## Description: <br>
Connects OpenClaw to the Clawhome chat platform so an agent can send, receive, and auto-reply to messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shengguo](https://clawhub.ai/user/shengguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure OpenClaw as a Clawhome chat connector for bidirectional text and file/image messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Channel secrets can be exposed through shared terminals, logs, or pasted command history. <br>
Mitigation: Treat channelSecret like a password, avoid sharing it, and rotate it if it is exposed. <br>
Risk: Uploaded files are sent to Clawhome through a documented upload flow that does not describe authentication, retention, deletion, or access controls. <br>
Mitigation: Upload only files that are appropriate to send to Clawhome and avoid sensitive files unless the service terms and controls are understood. <br>
Risk: The skill installs and configures an external OpenClaw plugin. <br>
Mitigation: Install only if you trust the openclaw-clawhome plugin source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shengguo/openclaw-clawhome) <br>
- [Clawhome file upload endpoint](https://www.clawhome.io/api/oss/upload) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw plugin installation, channel configuration, gateway restart, WebSocket topic, heartbeat, text message, and file message guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
