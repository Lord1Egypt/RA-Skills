## Description: <br>
Query real-time and historical financial data across equities and crypto prices, market moves, metrics, and trends for analysis, alerts, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and analysts use this skill to query AIsa market-data endpoints for equities, cryptocurrencies, company news, financial statements, analyst estimates, SEC filings, insider activity, ownership data, interest rates, and stock screening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The AISA API key and market research parameters are sent to AIsa's service. <br>
Mitigation: Use a dedicated API key, monitor quota or credit usage, and avoid sending confidential portfolio or trading-strategy details unless that sharing is acceptable. <br>
Risk: Live market-data calls may consume paid API credits. <br>
Mitigation: Review command parameters before execution and monitor response usage fields, quota, and remaining credits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xjordansg-yolo/openclaw-aisa-finance-stock-equity-crypto-market-price-data-yahoo-finance-coinhacko) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AIsa API reference](https://aisa.mintlify.app/api-reference/introduction) <br>
- [AIsa signup](https://aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with bash, curl, Python command examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl or python3 and an AISA_API_KEY environment variable for live API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
