## Description: <br>
Helps users connect an OpenClaw agent to DingTalk as an internal bot channel, configure Stream mode, and troubleshoot DingTalk message issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaoyunhao0107](https://clawhub.ai/user/shaoyunhao0107) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install and enable the DingTalk channel plugin, configure required DingTalk app credentials, restart the gateway, and diagnose common setup and message-delivery failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may install and trust a third-party DingTalk plugin package without confirming it is the intended package. <br>
Mitigation: Confirm that @soimy/dingtalk is the expected plugin before installation and review the plugin source or package metadata according to local trust policy. <br>
Risk: DingTalk app secrets may be exposed through command history, shared screenshots, or overly broad access to the OpenClaw configuration file. <br>
Mitigation: Prefer interactive configuration, avoid placing real secrets in commands or screenshots, restrict access to ~/.openclaw/openclaw.json, and rotate any secret that was copied into examples or shared channels. <br>
Risk: Open DM or group settings may allow broader bot access than intended in sensitive workspaces. <br>
Mitigation: Consider allowlist settings for direct messages and groups when deploying in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shaoyunhao0107/openclaw-skill-dingtalk-setup) <br>
- [DingTalk Plugin Repository](https://github.com/soimy/openclaw-channel-dingtalk) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [DingTalk Open Platform](https://open.dingtalk.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, configuration, verification, and troubleshooting guidance for OpenClaw DingTalk channel setup.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
