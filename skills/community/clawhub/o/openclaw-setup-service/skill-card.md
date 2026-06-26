## Description: <br>
OpenClaw安装服务 helps users install and configure OpenClaw, including WeChat, Feishu, and DingTalk channels plus heartbeat automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install OpenClaw, initialize a workspace, configure messaging channels, and set up heartbeat automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Global npm installation and registry changes may install untrusted code or pull from an unexpected package source. <br>
Mitigation: Verify the OpenClaw npm package and registry source before installation. <br>
Risk: Channel setup may expose QR sessions, App Secrets, or webhook credentials. <br>
Mitigation: Do not share sessions, secrets, or webhooks with support staff; use least-privilege channel credentials. <br>
Risk: Heartbeat automation may continue running after setup and perform recurring actions unexpectedly. <br>
Mitigation: Confirm how to stop heartbeat automation before enabling it. <br>
Risk: Paid setup support and cryptocurrency payment details may create purchase or fraud risk. <br>
Mitigation: Verify ClawMart and the service terms before paying, especially via cryptocurrency. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yang1002378395-cmyk/openclaw-setup-service) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw GitHub Issues](https://github.com/openclaw/openclaw/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps, channel configuration guidance, heartbeat automation instructions, troubleshooting notes, pricing, and support links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
