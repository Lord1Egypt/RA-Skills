## Description: <br>
Connect a local LM Studio model directly to Discord as a lightweight chat bot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dq-stack](https://clawhub.ai/user/dq-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and server operators use this skill to set up a lightweight Discord bot that forwards messages from a configured guild to a locally running LM Studio chat completions endpoint and replies in Discord. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bot can read messages in accessible Discord channels and send them to a local LM Studio service. <br>
Mitigation: Use a dedicated bot token, restrict the bot to trusted channels or a command trigger, and notify server members that messages may be processed by the local model. <br>
Risk: Message contents and model replies may be logged by the bot template or local service. <br>
Mitigation: Avoid sensitive conversations, review logging behavior before deployment, and run the bot only in environments where local logs are controlled. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dq-stack/lm-studio-discord) <br>
- [Discord Developer Portal](https://discord.com/developers/applications) <br>
- [Discord OAuth2 Bot Authorization URL](https://discord.com/oauth2/authorize?client_id=BOT_CLIENT_ID&permissions=1024&scope=bot) <br>
- [LM Studio Local Chat Completions Endpoint](http://127.0.0.1:1234/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with JavaScript code template references and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance for a single Discord bot instance using one configured LM Studio model.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
