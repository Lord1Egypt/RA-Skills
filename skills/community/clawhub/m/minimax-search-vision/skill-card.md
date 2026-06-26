## Description: <br>
MiniMax Search & Vision lets an agent run web searches and analyze images through the MiniMax Token Plan MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaolongliu1988](https://clawhub.ai/user/xiaolongliu1988) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add MiniMax-backed web search and image understanding to an agent. It supports search-result retrieval and prompt-based analysis of HTTP/HTTPS image URLs or local image files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, internal URLs, screenshots, local images, and other submitted content may be processed by the external MiniMax service. <br>
Mitigation: Avoid confidential inputs unless external MiniMax processing is acceptable for the use case. <br>
Risk: MiniMax API credentials could be exposed if stored or logged carelessly. <br>
Mitigation: Use a scoped MiniMax API key, keep the credential file private, and rely on environment variables or the documented private credential file. <br>
Risk: The skill depends on MiniMax, mcporter, and the MCP package it runs. <br>
Mitigation: Install and use the skill only when those third-party services and packages are trusted for the deployment. <br>


## Reference(s): <br>
- [MiniMax Platform](https://platform.minimaxi.com) <br>
- [MiniMax API Reference](references/minimax_api.md) <br>
- [Token Plan MCP Documentation](https://platform.minimaxi.com/docs/guides/token-plan-mcp-guide.md) <br>
- [MiniMax API Overview](https://platform.minimaxi.com/docs/api-reference/api-overview.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search or vision results with Markdown/plain-text guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MiniMax API key and mcporter; image inputs support HTTP/HTTPS URLs or local files up to 20 MB.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
