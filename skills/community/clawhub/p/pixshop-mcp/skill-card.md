## Description: <br>
Pixshop MCP connects Claude-compatible clients to Pixshop creative tools for image generation, photo editing, video creation, virtual try-on, face swap, style transfer, and visual effects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lizhijun](https://clawhub.ai/user/lizhijun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, designers, marketers, and developers use this skill to call Pixshop media-generation and editing tools from Claude Desktop, Cursor, or other MCP clients. It supports workflows such as prompt-assisted image generation, product imagery, portrait transformations, video generation, and publishing Pixshop content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill configures a persistent remote MCP service that can receive prompts, image URLs, portraits, product assets, and generated media. <br>
Mitigation: Use it only with media you are allowed to send to Pixshop, avoid confidential or sensitive images unless Pixshop's privacy and retention terms have been reviewed, and limit client permissions where supported. <br>
Risk: Creative-media operations can spend Pixshop credits, including higher-cost video and generation workflows. <br>
Mitigation: Require explicit user confirmation before invoking credit-consuming actions and monitor account credit usage. <br>
Risk: The skill includes publishing and remix workflows that may make generated content visible on Pixshop. <br>
Mitigation: Confirm publication intent, title, description, and rights to source media before using publishing or remix tools. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/lizhijun/pixshop-mcp) <br>
- [Pixshop](https://pixshop.app) <br>
- [Pixshop MCP endpoint](https://pixshop.app/api/mcp) <br>
- [Pixshop apps](https://pixshop.app/apps) <br>
- [Pixshop prompt library](https://pixshop.app/prompt-library) <br>
- [Pixshop pricing](https://pixshop.app/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON MCP configuration and natural-language tool usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference remote Pixshop media URLs, prompts, account credits, and generated image or video assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
