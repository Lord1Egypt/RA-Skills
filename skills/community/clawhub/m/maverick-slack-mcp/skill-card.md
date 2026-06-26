## Description: <br>
Search, read, and update Slack messages, channel history, canvases, and users through Slack's hosted MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover Slack's hosted MCP tool catalog, search or read Slack workspace content, and perform user-confirmed updates such as sending messages or changing canvases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change Slack content using the connected user's OAuth token. <br>
Mitigation: Review granted Slack scopes and require clear user confirmation before posting, editing, or creating Slack content. <br>
Risk: Tool arguments and results transit Slack's hosted MCP server. <br>
Mitigation: Avoid passing unrelated sensitive content through Slack tool arguments. <br>
Risk: The OAuth grant can persist after the user stops using the skill. <br>
Mitigation: Revoke the Slack grant when access is no longer needed. <br>


## Reference(s): <br>
- [Slack MCP server documentation](https://docs.slack.dev/ai/slack-mcp-server/) <br>
- [mcporter config reference](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md) <br>
- [ClawHub skill page](https://clawhub.ai/maverick/maverick-slack-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Slack MCP tool outputs; externally visible write actions require clear user confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
