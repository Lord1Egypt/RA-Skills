## Description: <br>
Uses the MiniMax MCP web_search tool to perform online searches when an agent needs current news, information, or web lookup results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Thincher](https://clawhub.ai/user/Thincher) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agent users and developers use this skill to route web search requests through MiniMax MCP and return search results for a single query. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup can expose or persist a MiniMax API key in plaintext. <br>
Mitigation: Use a dedicated MiniMax API key with limited billing exposure, prefer a secure secret mechanism or environment variable, and avoid commands that print the key. <br>
Risk: Search queries are sent to an external MiniMax service. <br>
Mitigation: Do not place private, regulated, or sensitive data in search queries unless the deployment has approved that use. <br>
Risk: The skill installs and runs external tooling before performing searches. <br>
Mitigation: Verify the uv installer and minimax-coding-plan-mcp package source before installing or running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Thincher/minimax-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown instructions and formatted JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MiniMax API key and sends one query string to the MiniMax MCP web_search tool.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
