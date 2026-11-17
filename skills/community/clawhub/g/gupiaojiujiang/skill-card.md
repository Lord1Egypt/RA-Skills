## Description:

股票九剑 analyzes A-share stock codes by fetching market data, computing technical features, matching a nine-pattern rule framework, and returning a concise short-term trading assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhc2026](https://clawhub.ai/user/yhc2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to evaluate A-share stock codes with a structured technical-analysis workflow, optional chart generation, and risk-aware commentary. The output is analysis support and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts market-data sources through akshare and depends on external Python packages.

Mitigation: Install it in a dedicated virtual environment, consider pinning dependencies, avoid elevated shells, and allow only expected market-data network access.

Risk: Chart generation may write PNG files to the local workspace.

Mitigation: Use a dedicated workspace and review generated chart paths before retaining or sharing outputs.

Risk: Stock-analysis output may be mistaken for investment advice.

Mitigation: Treat outputs as analysis support, verify them against current market data, and use qualified financial judgment before making decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yhc2026/skills/gupiaojiujiang)
- [股票九剑 framework](knowledge/framework.md)
- [MCP platform configuration guide](mcp_server/PLATFORM_CONFIGS.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, files, guidance]

**Output Format:** [Markdown-style stock analysis report, JSON-compatible MCP tool responses, and optional PNG chart file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live or recent A-share market data via akshare and may write chart PNG files when chart generation is requested.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
