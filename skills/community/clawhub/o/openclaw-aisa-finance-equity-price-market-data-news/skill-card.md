## Description: <br>
Query real-time and historical financial data for equities: prices, news, financial statements, metrics, analyst estimates, insider and institutional activity, SEC filings, earnings press releases, segmented revenues, stock screening, and macro interest rates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to query AIsa market-data endpoints and CLI helpers for equity research, market screening, filings review, company news, ownership analysis, earnings context, and reporting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends market-data queries and an AISA API key to a third-party provider. <br>
Mitigation: Use a dedicated key where possible, monitor credit usage, and avoid sending confidential watchlists or regulated research data unless the organization approves AIsa. <br>
Risk: API calls can consume pay-as-you-go credits. <br>
Mitigation: Review planned queries before execution and monitor response usage fields such as cost and credits remaining. <br>
Risk: Earnings press release coverage is narrower than other financial endpoints and unsupported tickers return errors. <br>
Mitigation: Check the supported ticker list before relying on the earnings press release endpoint, and use analyst estimates or financial statements as alternatives when needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aisadocs/openclaw-aisa-finance-equity-price-market-data-news) <br>
- [AIsa Homepage](https://aisa.one) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>
- [Earnings Press Releases Supported Tickers](./earnings-press-releases-tickers.md) <br>
- [financialdatasets.ai earnings press releases tickers](https://api.financialdatasets.ai/earnings/press-releases/tickers) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with curl and Python command examples; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; responses may include usage cost and remaining credits.] <br>

## Skill Version(s): <br>
2.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
