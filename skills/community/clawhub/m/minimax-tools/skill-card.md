## Description: <br>
This skill lets agents use MiniMax tools to analyze images and run web searches for current information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OujaKivi](https://clawhub.ai/user/OujaKivi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route image-understanding requests and web-search queries through MiniMax MCP tools from an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, prompts, and search queries may be sent to MiniMax through the MCP package. <br>
Mitigation: Avoid sending sensitive local images or confidential queries unless they are approved for MiniMax processing. <br>
Risk: The MiniMax API key may be stored in a plaintext configuration file. <br>
Mitigation: Prefer an environment variable or secret manager, and restrict permissions on any local config file. <br>
Risk: Setup relies on uv or uvx to install and run the minimax-coding-plan-mcp package. <br>
Mitigation: Verify the uv installer and MCP package before running them, and pin versions where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OujaKivi/minimax-tools) <br>
- [MiniMax API host](https://api.minimaxi.com) <br>
- [MiniMax coding plan subscription](https://platform.minimaxi.com/subscribe/coding-plan?code=GjuAjhGKqQ&source=link) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [JSON or plain text emitted by Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and the uvx-run minimax-coding-plan-mcp package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
