## Description:

Natural language screener for investment assets across global markets, including A-shares, ETFs, bonds, HK and US stocks, and funds, using Eastmoney Miaoxiang data to return CSV results and a data description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akiry09](https://clawhub.ai/user/akiry09)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and financial analysts use this skill to screen stocks, funds, ETFs, bonds, and sectors with natural language queries across supported markets. It helps produce local CSV exports and short descriptions for market monitoring, portfolio research, and strategy analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, select type, and EM_API_KEY are sent to the EastMoney service.

Mitigation: Confirm trust in the EastMoney service before installing, scope the API key appropriately, and rotate or revoke it if exposure is suspected.

Risk: Generated CSV files contain remote market data that is not formula-sanitized.

Mitigation: Open exported CSV files carefully, especially in spreadsheet software, and inspect or sanitize data before sharing or automated processing.

Risk: Screening results may be mistaken for investment advice.

Mitigation: Treat outputs as market-screening data for research and validate decisions with qualified financial review.

## Reference(s):

- [Mx Stocks Screener on ClawHub](https://clawhub.ai/akiry09/skills/mx-mx-stocks-screener)
- [Eastmoney Miaoxiang API registration](https://ai.eastmoney.com/mxClaw)
- [Eastmoney selectSecurity API endpoint](https://ai-saas.eastmoney.com/proxy/b/mcp/tool/selectSecurity)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell and Python examples; runtime output writes UTF-8 CSV and text description files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY; optional MX_STOCKS_SCREENER_OUTPUT_DIR controls where CSV and description files are written.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
