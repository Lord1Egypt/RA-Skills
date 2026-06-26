## Description: <br>
Configure Feishu as an OpenClaw messaging channel in 15 minutes, enabling single and group chat with event subscription and secure API integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a Feishu bot as an OpenClaw message channel, including app creation, permissions, event subscription, gateway startup, and group-chat options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu App Secret, verification token, encryption key, and OpenClaw config values can expose account or workspace access if shared or committed. <br>
Mitigation: Use a dedicated Feishu app, protect ~/.openclaw/config.yaml, avoid committing secrets, grant only the listed permissions, and rotate the App Secret if exposure is suspected. <br>
Risk: Public webhook or tunnel endpoints used for event subscription can expose the OpenClaw gateway beyond the local network. <br>
Mitigation: Enable verification and encryption values where available, restrict the app availability scope, monitor public tunnels, and close tunnel sessions when setup or testing is complete. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yang1002378395-cmyk/openclaw-feishu-setup) <br>
- [Feishu Open Platform app console](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, markdown] <br>
**Output Format:** [Markdown with YAML configuration examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only setup guidance for configuring Feishu credentials, event subscriptions, OpenClaw gateway startup, and optional tunnel choices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact package.json, artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
