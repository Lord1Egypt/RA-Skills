## Description: <br>
Access real-time stock prices, historical data, company fundamentals, financial statements, and earnings for any stock symbol using Alpha Vantage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-data workflows use this skill to query Alpha Vantage quotes, daily price history, company fundamentals, financial statements, balance sheets, and earnings through a Pipeworx-hosted MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests to the external Pipeworx-hosted MCP gateway may reveal confidential watchlists, trading plans, or proprietary research context. <br>
Mitigation: Use only non-confidential market-data queries unless the user is comfortable sharing that query context with the external provider. <br>


## Reference(s): <br>
- [Pipeworx alphavantage ClawHub page](https://clawhub.ai/brucegutman/pipeworx-alphavantage) <br>
- [Alpha Vantage MCP endpoint](https://gateway.pipeworx.io/alphavantage/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP server configuration JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces market-data lookup guidance and an MCP server endpoint configuration for agent use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
