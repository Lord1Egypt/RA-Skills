## Description: <br>
Generate images, audio, and video using MiniMax MCP and send the resulting media to Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoyin258](https://clawhub.ai/user/hoyin258) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to configure MiniMax MCP, generate media assets, and deliver full MiniMax media URLs to Telegram chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MiniMax API keys and tokenized media URLs can expose credentials or temporary access tokens if shared in chats or logs. <br>
Mitigation: Keep the MiniMax API key private, avoid logging secrets, and treat full MiniMax media URLs as sensitive until they expire. <br>
Risk: Third-party package installation and MCP server setup can introduce supply-chain risk. <br>
Mitigation: Verify mcporter and minimax-mcp package sources before installation and prefer pinned versions where practical. <br>
Risk: Generated media may be sent to the wrong Telegram chat. <br>
Mitigation: Confirm the Telegram target chat before sending generated media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hoyin258/minimax-to-telegram) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and Python-style examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers MiniMax MCP setup, media generation parameters, Telegram message calls, and use of full tokenized media URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
