## Description: <br>
MiniMax MCP tools provide web search and image understanding through MiniMax Coding Plan for agents that need current information or image analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[russellfei](https://clawhub.ai/user/russellfei) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to call MiniMax MCP tools for web search, current-information retrieval, and image understanding from an OpenClaw-compatible agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup documentation uses installer commands that fetch and execute remote uv install scripts. <br>
Mitigation: Review setup commands before installation and prefer installing uv through a trusted package manager or verified installer. <br>
Risk: The wrapper loads variables from ~/.openclaw/.env and passes the process environment to the MCP child process. <br>
Mitigation: Store the MiniMax API key with restrictive file permissions and avoid placing unrelated secrets in ~/.openclaw/.env. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/russellfei/minimax-mcp-call) <br>
- [MiniMax Platform](https://platform.minimaxi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Command-line output and JSON responses from MiniMax MCP tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and a Node.js/uv runtime.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
