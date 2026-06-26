## Description: <br>
Use MiniMax Coding Plan API for real-time web search and image understanding (VLM). Based on yorch233/minimax-coding-plan-tool, patched to use api.minimax.io instead of api.minimax.chat. No external MCP servers needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jlin53882](https://clawhub.ai/user/jlin53882) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent perform MiniMax-backed web search and image understanding from shell commands or OpenClaw tool calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, image URLs, prompts, and selected local image files are sent to MiniMax for online processing. <br>
Mitigation: Do not submit secrets, confidential documents, private screenshots, or internal-only URLs unless external MiniMax processing is approved. <br>
Risk: Local image files passed to the image understanding command are read and converted to base64 before API submission. <br>
Mitigation: Review image paths before execution and use only files intended for external analysis. <br>


## Reference(s): <br>
- [MiniMax Platform](https://platform.minimaxi.com) <br>
- [Original ClawHub Skill](https://clawhub.ai/yorch233/minimax-coding-plan-tool) <br>
- [Publisher Profile](https://clawhub.ai/user/jlin53882) <br>
- [ClawHub Skill Page](https://clawhub.ai/jlin53882/minimax-coding-plan-tool-patched) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses and Markdown documentation with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Web search returns structured result objects; image understanding returns text analysis from a URL or supported local image file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
