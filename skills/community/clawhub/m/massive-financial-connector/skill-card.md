## Description:

Massive Financial Connector connects agents to Massive/Polygon market data through the official MCP server and quick shell scripts for stock, options, forex, crypto, and indices queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[virtual-ny](https://clawhub.ai/user/virtual-ny)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to query real-time and historical market data from Massive/Polygon, discover endpoints, inspect endpoint docs, call APIs, run SQL-style table queries, and perform common quote checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs Massive MCP server code from GitHub at launch time.

Mitigation: Pin the MCP dependency to an immutable commit or verified package and review it before deployment.

Risk: The helper scripts handle MASSIVE_API_KEY through shell startup files and URL query parameters.

Mitigation: Provide the key only through the invoking environment, remove shell startup file sourcing, and avoid URL-query API keys in sensitive environments.

Risk: Market-data output may be used in investment-style prompts.

Mitigation: Keep the skill's non-advice disclaimer and require users to make independent financial decisions.

## Reference(s):

- [Massive MCP server repository](https://github.com/massive-com/mcp_massive/tree/v0.4.0)
- [ClawHub skill page](https://clawhub.ai/virtual-ny/skills/massive-financial-connector)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise market-data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MASSIVE_API_KEY and may invoke local shell scripts or the Massive MCP server.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
