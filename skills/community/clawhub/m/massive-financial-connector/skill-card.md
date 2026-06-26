## Description: <br>
Massive Financial Connector provides Massive (Polygon) market-data access through an official MCP server and quick scripts for endpoint discovery, endpoint docs, generic API calls, SQL-style table querying, post-processing, and common stock, options, forex, crypto, and index quote checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[virtual-ny](https://clawhub.ai/user/virtual-ny) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to query Massive/Polygon market data through an MCP server or quick shell scripts for stock, options, forex, crypto, and index checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts source the user's ~/.zshrc before reading MASSIVE_API_KEY, which can run shell startup commands during skill execution. <br>
Mitigation: Review the scripts before installation and prefer requiring MASSIVE_API_KEY from the current environment or a dedicated config file. <br>
Risk: The skill uses a local Massive API key in shell scripts and an uvx-launched MCP server. <br>
Mitigation: Use a revocable or limited API key and avoid printing, committing, or uploading credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/virtual-ny/massive-financial-connector) <br>
- [Massive MCP Server Repository](https://github.com/massive-com/mcp_massive) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and concise market-data results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns numeric market-data results first, then timestamp and exchange metadata when available.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
