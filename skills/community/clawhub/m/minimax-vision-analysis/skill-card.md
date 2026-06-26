## Description: <br>
MiniMax Vision Analysis helps agents analyze images with the MiniMax vision MCP tool for descriptions, OCR, UI review, chart data extraction, and object or activity identification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daidai8910g](https://clawhub.ai/user/daidai8910g) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route image-analysis requests to MiniMax for image descriptions, text extraction, UI critique, chart interpretation, and object detection. It is useful when a user provides an image file path, image URL, screenshot, diagram, chart, mockup, wireframe, or photo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images, image references, private URLs, or local paths may be sent to MiniMax for processing. <br>
Mitigation: Avoid analyzing confidential screenshots, documents, private URLs, or local files unless the user intends to share them with MiniMax. <br>
Risk: The skill requires configuring an external MiniMax MCP package and API key. <br>
Mitigation: Protect MINIMAX_API_KEY, verify the MCP package before setup, and install only when the user is comfortable with the MiniMax integration. <br>
Risk: Vision analysis can produce incomplete or misleading descriptions, OCR, or extracted chart data. <br>
Mitigation: Review image-analysis results before using them for decisions or publishing extracted information. <br>


## Reference(s): <br>
- [MiniMax Token Plan MCP Guide](https://platform.minimaxi.com/docs/token-plan/mcp-guide) <br>
- [ClawHub Release Page](https://clawhub.ai/daidai8910g/minimax-vision-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown prose with structured sections and inline code blocks when setup guidance is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OCR text, design-review findings, chart summaries, object lists, or MCP setup commands depending on the selected analysis mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
