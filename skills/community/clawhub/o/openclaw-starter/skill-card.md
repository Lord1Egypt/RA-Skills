## Description: <br>
OpenClaw Starter guides new OpenClaw users through skill recommendations, channel setup, document templates, and first-use questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[testmtcode](https://clawhub.ai/user/testmtcode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill after installation to choose starter skills, configure Telegram, WhatsApp, Discord, or WebChat, and create common OpenClaw workspace documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may recommend bulk-installing other skills, including automation or code-running tools. <br>
Mitigation: Review recommended skills and their security scans before installing them, especially tools involving SSH, Docker, email, webhooks, or code execution. <br>
Risk: Messaging-channel setup can expose Telegram or Discord tokens, or link a WhatsApp account to OpenClaw. <br>
Mitigation: Keep tokens out of source control, logs, screenshots, and shared chats; prefer environment variables or the OpenClaw configuration flow, and know how to revoke linked messaging sessions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/testmtcode/openclaw-starter) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Telegram Bot API](https://core.telegram.org/bots/api) <br>
- [Discord developer documentation](https://discord.com/developers/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend installing other skills and configuring messaging-channel credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
