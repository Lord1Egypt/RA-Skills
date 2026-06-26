## Description: <br>
OpenClaw complete documentation knowledge base covering installation, configuration, Gateway management, channels, nodes, CLI commands, automation, security, and other core functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Aetik-yue](https://clawhub.ai/user/Aetik-yue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill as reference documentation for OpenClaw installation, configuration, Gateway and channel setup, CLI commands, automation, security, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shown commands can install packages, enable daemons, start a Gateway, or configure remote access if a user runs them directly. <br>
Mitigation: Verify the OpenClaw package and documentation before running commands, and avoid enabling daemons or remote access unless the environment is intended for that use. <br>
Risk: Channel and device setup can expose accounts, messages, or devices when authorization is too broad. <br>
Mitigation: Connect only accounts and devices the user owns or is authorized to manage, and use allowlists plus strong authentication. <br>
Risk: Hooks, webhooks, memory, and remote-access settings can affect privacy and security. <br>
Mitigation: Review these settings before deployment and limit them to the minimum access needed. <br>


## Reference(s): <br>
- [OpenClaw Documentation](https://docs.openclaw.ai/zh-CN) <br>
- [OpenClaw Documentation Index](https://docs.openclaw.ai/llms.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/Aetik-yue/openclaw-relation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only reference output; the skill does not install or run code itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
