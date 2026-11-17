## Description:

Microsoft Ads MCP helps agents create and manage Microsoft Advertising campaigns through an MCP server, including campaigns, ad groups, keywords, ads, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bit-of-a-shambles](https://clawhub.ai/user/bit-of-a-shambles)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to connect an agent to a Microsoft Advertising MCP server for account lookup, campaign setup, keyword and ad management, and performance reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned third-party MCP server code can access Microsoft Ads credentials.

Mitigation: Use a pinned, audited server version in an isolated environment and authorize only a least-privilege Microsoft Ads identity.

Risk: Campaign activation, budget changes, ad publishing, and report exports can affect live ad spend or expose business data.

Mitigation: Require human confirmation for spend-bearing or export actions, avoid administrator credentials, and keep campaigns paused until reviewed.

## Reference(s):

- [Microsoft Ads MCP server homepage](https://github.com/Duartemartins/microsoft-ads-mcp-server)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Bing Ads Python SDK](https://github.com/BingAds/BingAds-Python-SDK)
- [Microsoft Advertising](https://ads.microsoft.com)
- [Microsoft Advertising Developer](https://developers.ads.microsoft.com)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coordinate MCP tool calls that return account, campaign, ad group, keyword, ad, budget, label, and report data.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
