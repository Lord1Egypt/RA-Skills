## Description: <br>
Connects OpenClaw AI agents to WeCom so they can receive and send enterprise chat messages, with message encryption, token management, and access-control settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darrryZ](https://clawhub.ai/user/darrryZ) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to add a WeCom channel for enterprise messaging, including inbound text callbacks and outbound plain-text replies or pushes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enterprise chat content may appear in OpenClaw or gateway logs. <br>
Mitigation: Restrict access to OpenClaw and gateway logs, and avoid sending regulated or confidential data unless logs are controlled or redacted. <br>
Risk: WeCom credentials and callback secrets are required for operation. <br>
Mitigation: Store the WeCom corpId, agent secret, callback token, and EncodingAESKey in a secrets manager or tightly permissioned configuration. <br>
Risk: Pairing access control is advertised but was not clearly enforced in the inspected message handler. <br>
Mitigation: Use allowlist mode or verify pairing enforcement before installing the skill in a business WeCom workspace. <br>


## Reference(s): <br>
- [OpenClaw WeCom Channel on ClawHub](https://clawhub.ai/darrryZ/openclaw-wecom-channel) <br>
- [OpenClaw WeCom Channel project homepage](https://github.com/darrryZ/openclaw-wecom-channel) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [WeCom Developer Documentation](https://developer.work.weixin.qq.com/document/) <br>
- [WeCom callback encryption documentation](https://developer.work.weixin.qq.com/document/path/90968) <br>
- [WeCom message send API documentation](https://developer.work.weixin.qq.com/document/path/90236) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command snippets; runtime channel output is plain-text WeCom messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node, network access, OpenClaw, and WeCom application credentials; the channel supports direct plain-text messages only.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
