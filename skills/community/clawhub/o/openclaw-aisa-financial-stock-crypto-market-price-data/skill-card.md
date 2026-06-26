## Description: <br>
Query real-time and historical financial data across equities and crypto--prices, market moves, metrics, and trends for analysis, alerts, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to query AIsa market-data endpoints for equity and cryptocurrency prices, company financials, news, analyst data, SEC filings, screeners, and related market context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-data queries and API credentials are sent to AIsa, including tickers, dates, screener filters, and portfolio-style symbol lists. <br>
Mitigation: Use a dedicated or limited AISA_API_KEY and avoid submitting sensitive portfolio or strategy details unless the user accepts that disclosure. <br>
Risk: Provider-side API calls may be logged or consume credits. <br>
Mitigation: Monitor API usage, keep credit limits appropriate for the deployment, and confirm requests before running broad or repeated queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xjordansg-yolo/openclaw-aisa-financial-stock-crypto-market-price-data) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/0xjordansg-yolo) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AIsa API reference](https://aisa.mintlify.app/api-reference/introduction) <br>
- [Skill documentation](SKILL.md) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and network access to AIsa market-data APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
