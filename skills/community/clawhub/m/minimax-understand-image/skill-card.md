## Description: <br>
Uses the MiniMax MCP server to analyze images, describe visual content, and answer prompts about objects, text, and scenes in an image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Thincher](https://clawhub.ai/user/Thincher) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to send a local image path or image URL plus a prompt to MiniMax's image-understanding MCP tool and receive structured analysis. It is useful for describing image contents and identifying visible objects, text, and scenes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images and prompts are sent to the MiniMax cloud service. <br>
Mitigation: Use the skill only with images and prompts that are appropriate to share with MiniMax, and avoid sensitive or regulated content unless the deployment has approved terms and controls. <br>
Risk: The setup flow may inspect a local auth profile store for MiniMax credentials. <br>
Mitigation: Prefer setting MINIMAX_API_KEY explicitly and require user confirmation before reusing any credential found in local profile files. <br>
Risk: The skill installs and runs an unpinned external MCP package through uvx. <br>
Mitigation: Verify the minimax-coding-plan-mcp package source and version before execution, and pin or mirror a reviewed version for managed deployments. <br>
Risk: The documented fallback configuration can store the MiniMax API key in a plaintext local file. <br>
Mitigation: Protect file permissions, avoid plaintext storage where possible, and rotate the key if the local config may have been exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Thincher/minimax-understand-image) <br>
- [Publisher profile](https://clawhub.ai/user/Thincher) <br>
- [MiniMax API host used by the skill](https://api.minimaxi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses and terminal output, with Markdown setup instructions in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an image path or URL, a prompt, uvx, the minimax-coding-plan-mcp package, and a MiniMax API key.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
