## Description: <br>
MiniMax MCP Search performs real-time web searches and image understanding through MiniMax MCP using user prompts and image sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hillsp99](https://clawhub.ai/user/hillsp99) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can use this skill to retrieve concise web search results or ask for descriptions and analysis of local or URL-based images. It is intended for workflows that need current search context or image understanding from MiniMax MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports that crafted user input could run unintended local shell commands through the wrapper. <br>
Mitigation: Review before installing, use only trusted inputs, and avoid sensitive prompts, private URLs, or local image paths unless the MiniMax and MCP tooling path is approved. <br>
Risk: The skill depends on external MiniMax MCP tooling, mcporter, and API key configuration. <br>
Mitigation: Verify the mcporter package source and API key configuration before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hillsp99/minimax-mcp-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON objects containing search result lists or image descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include titles, links, summaries, and dates; image output includes a generated description and source reference.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.json, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
