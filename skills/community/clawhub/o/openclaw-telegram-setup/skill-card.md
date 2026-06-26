## Description: <br>
Guides agents through configuring a Telegram Bot as an OpenClaw message channel with chat ID, group, command, and webhook setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to connect Telegram to OpenClaw for personal or group AI messaging, including command setup and optional webhook configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens can grant access to the bot if exposed. <br>
Mitigation: Treat the bot token like a password, keep OpenClaw configuration files out of version control, and rotate the token if it is exposed. <br>
Risk: Incorrect chat allowlists or webhook settings can route messages to unintended chats or infrastructure. <br>
Mitigation: Restrict allowedChatIds to trusted personal or group chats and use webhook mode only with HTTPS infrastructure you control. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yang1002378395-cmyk/openclaw-telegram-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance only; users must supply their own Telegram bot token and OpenClaw configuration values.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
