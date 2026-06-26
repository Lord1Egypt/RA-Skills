## Description: <br>
MiniMax MCP server for web search and image understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TangUsers](https://clawhub.ai/user/TangUsers) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to call MiniMax-backed MCP tools for web search, URL-oriented information lookup, and image understanding workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends searches, URLs, prompts, or images to MiniMax services. <br>
Mitigation: Only submit content that is appropriate to share with MiniMax and follow the user's data-handling requirements. <br>
Risk: Using MiniMax tools may incur API usage costs. <br>
Mitigation: Use a dedicated MiniMax API key where possible and monitor account usage. <br>
Risk: The MCP server depends on uvx and external installer paths. <br>
Mitigation: Prefer the Homebrew uv installation path or verify the uv installer before use. <br>
Risk: MiniMax API keys must match the selected regional API host. <br>
Mitigation: Configure MINIMAX_API_KEY and MINIMAX_API_HOST together for the same MiniMax region before testing the server. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TangUsers/minimax-mcp) <br>
- [MiniMax MCP usage examples](references/examples.md) <br>
- [MiniMax platform](https://www.minimax.io) <br>
- [MiniMax platform (China)](https://platform.minimaxi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require MiniMax API credentials and region-matched API host configuration.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
