## Description: <br>
mcp-storyboard helps agents generate multi-scene storyboard, story scene, and picture-book images through the BizyAir API, with prompt enhancement, aspect-ratio controls, batch generation, and asynchronous polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bozoyan](https://clawhub.ai/user/bozoyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create storyboard frames, story scene images, and picture-book illustrations from natural-language prompts. It is suited for workflows that need generated image URLs, Markdown-ready results, configurable aspect ratios, and limited batch creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and the BizyAir API key are sent to BizyAir during image generation. <br>
Mitigation: Avoid sensitive story details in prompts and use safer secret storage for the API key instead of long-lived shell startup configuration. <br>
Risk: The skill can automatically append sexualized person-specific prompt text to broad character, children, or picture-book requests. <br>
Mitigation: Review or disable the automatic model prompt suffix before ordinary character, children, or picture-book use. <br>
Risk: Batch image generation can create long-running external API tasks and spend more quota than intended. <br>
Mitigation: Set batch size explicitly, keep generation limits small, and monitor the asynchronous polling output. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bozoyan/mcp-storyboard) <br>
- [Publisher profile](https://clawhub.ai/user/bozoyan) <br>
- [BizyAir MCP endpoint](https://api.bizyair.cn/w/v1/mcp/242) <br>
- [BizyAir asynchronous task API](https://api.bizyair.cn/w/v1/webapp/task/openapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with image URLs, progress messages, and error guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return generated image URLs and preview-ready Markdown; image generation can take 3-10 minutes and polls for up to 15 minutes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact package.json and MCP server report 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
