## Description: <br>
MiniMax MCP Tools helps an OpenClaw agent configure and use MiniMax MCP web search and image understanding tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect an agent to MiniMax MCP tools for live web search and image-content analysis. It provides setup guidance, MCP configuration, validation commands, and example tool calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes searches, image URLs, local image paths, and prompts through a third-party MiniMax MCP service. <br>
Mitigation: Use it only when third-party processing is acceptable, and avoid sending confidential searches, private images, or sensitive local file paths. <br>
Risk: The MCP configuration requires a MINIMAX_API_KEY secret. <br>
Mitigation: Keep the MCP configuration file private, store the API key as a secret, and avoid committing it to repositories or shared logs. <br>
Risk: The setup depends on the external minimax-coding-plan-mcp package. <br>
Mitigation: Install only if the publisher and package source are trusted, and review package behavior before using it in sensitive environments. <br>


## Reference(s): <br>
- [MiniMax MCP Tools on ClawHub](https://clawhub.ai/hongjiahao371-pixel/minimax-mcp-tools) <br>
- [MiniMax Token Plan](https://platform.minimaxi.com/subscribe/token-plan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP server configuration, environment variable names, setup checks, and example MiniMax tool calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
