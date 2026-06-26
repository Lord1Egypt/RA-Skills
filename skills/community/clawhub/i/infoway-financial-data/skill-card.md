## Description: <br>
Real-time financial market data MCP server — stocks, crypto, forex quotes, klines, sector analysis and fundamentals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infoway-api](https://clawhub.ai/user/infoway-api) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this MCP server to give AI assistants access to real-time quotes, klines, market depth, sector analysis, and company fundamentals across equities, crypto, and forex. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server requires an Infoway API key and sends market-data requests to Infoway. <br>
Mitigation: Install only where Infoway API-key use and outbound Infoway access are acceptable; use environment-specific keys and rotate them if exposed. <br>
Risk: Financial data and agent-generated analysis can be time-sensitive or incomplete. <br>
Mitigation: Verify critical quotes, fundamentals, and analysis against authoritative sources before relying on them for trading or business decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/infoway-api/infoway-financial-data) <br>
- [Infoway API](https://infoway.io) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Configuration] <br>
**Output Format:** [Text responses containing formatted JSON from MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires INFOWAY_API_KEY and outbound access to Infoway.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
