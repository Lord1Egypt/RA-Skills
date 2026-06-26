## Description: <br>
A wrapper that lets OpenClaw agents run MiniMax Token Plan web search through a local MCP package, with fallback guidance for Brave Search and Qwen Chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godiao](https://clawhub.ai/user/godiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using OpenClaw use this skill to issue web search queries through their MiniMax subscription without relying on uvx, and to fall back to Brave Search or Qwen Chat when MiniMax is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may be sent to MiniMax or fallback search providers. <br>
Mitigation: Do not search for secrets, credentials, regulated data, or confidential business information. <br>
Risk: The skill runs a local Python MCP package and depends on the configured Python interpreter. <br>
Mitigation: Pin and verify the minimax-coding-plan-mcp package version and set MINIMAX_PYTHON to a trusted interpreter. <br>
Risk: MiniMax API credentials are required for normal operation. <br>
Mitigation: Provide MINIMAX_API_KEY through OpenClaw environment variables and avoid storing credentials in config files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godiao/minimax-websearch) <br>
- [Publisher profile](https://clawhub.ai/user/godiao) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search result objects with Markdown usage and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output includes the original query, result count, result entries, and related queries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, created 2026-03-24) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
