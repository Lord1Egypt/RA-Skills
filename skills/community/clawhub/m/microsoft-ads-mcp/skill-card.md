## Description: <br>
Create and manage Microsoft Advertising campaigns (Bing Ads / DuckDuckGo Ads) via MCP server - campaigns, ad groups, keywords, ads, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bit-of-a-shambles](https://clawhub.ai/user/bit-of-a-shambles) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External marketers, developers, and campaign operators use this skill to connect an agent to a Microsoft Ads MCP server for managing search ad accounts, campaigns, ad groups, keywords, ads, and performance reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control real Microsoft Ads campaigns, including budgets, campaign status, ads, keywords, and reporting. <br>
Mitigation: Test with paused or low-budget campaigns and require explicit human confirmation before creating ads, changing budgets, or activating campaigns. <br>
Risk: The workflow relies on external MCP server code and Python dependencies. <br>
Mitigation: Inspect the linked MCP server code and requirements, install it in an isolated Python environment, and review dependencies before use. <br>
Risk: Microsoft Ads and Azure credentials are required and may be referenced from mcporter configuration. <br>
Mitigation: Protect the mcporter configuration, limit credential scope where possible, and rotate tokens if configuration files are exposed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/bit-of-a-shambles/microsoft-ads-mcp) <br>
- [Microsoft Ads MCP Server](https://github.com/Duartemartins/microsoft-ads-mcp-server) <br>
- [FastMCP](https://github.com/jlowin/fastmcp) <br>
- [Bing Ads Python SDK](https://github.com/BingAds/BingAds-Python-SDK) <br>
- [Microsoft Advertising](https://ads.microsoft.com) <br>
- [Microsoft Advertising Developer Portal](https://developers.ads.microsoft.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter, a Microsoft Ads account, a developer token, Azure AD app credentials, and access to the external MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
