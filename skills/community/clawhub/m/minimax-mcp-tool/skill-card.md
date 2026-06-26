## Description: <br>
Provides MiniMax-backed web search and image understanding for agents, with fallback options for Brave Search and Qwen Chat when MiniMax is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godiao](https://clawhub.ai/user/godiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using OpenClaw use this skill to run MiniMax-backed web search and image understanding from an agent after configuring their own MiniMax credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and image-analysis inputs may be sent to external providers. <br>
Mitigation: Use the skill only with content approved for those providers, and avoid private screenshots, credentials, personal data, internal documents, and sensitive research queries. <br>
Risk: Fallback behavior can change which external provider receives a request. <br>
Mitigation: Review the configured provider path before use and disclose or disable fallback routes when data-handling requirements restrict provider choice. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/godiao/minimax-mcp-tool) <br>
- [Publisher Profile](https://clawhub.ai/user/godiao) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; runtime tool output may be JSON search results or plain-text image descriptions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided MiniMax credentials; image understanding can process local image paths or image URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
