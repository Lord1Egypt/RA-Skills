## Description: <br>
金十数据 helps agents query Jin10 financial market quotes, K-line data, flash updates, news, and economic calendar data through a bundled Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robinspt](https://clawhub.ai/user/robinspt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve Jin10 market quotes, K-line/candlestick data, financial flash updates, news details, and economic calendar events. It is useful when a workflow needs structured or readable financial data from Jin10 using an API token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JIN10 API token and sends requests to the Jin10 MCP endpoint. <br>
Mitigation: Use a limited-purpose token, avoid exposing it in prompts or logs, and revoke it when the skill is no longer needed. <br>
Risk: The security summary notes a manifest transparency gap despite a clean verdict. <br>
Mitigation: Review the skill manifest and requested environment variables before installation, and prefer updated releases that tighten manifest permissions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/robinspt/jin10) <br>
- [Publisher Profile](https://clawhub.ai/user/robinspt) <br>
- [Jin10 API Token Setup](https://mcp.jin10.com/app) <br>
- [Jin10 MCP Endpoint](https://mcp.jin10.com/mcp) <br>
- [Jin10 API Contract](references/api-contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or text from CLI calls, with Markdown guidance and shell command examples in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JIN10_API_TOKEN and network access to the Jin10 MCP endpoint] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
