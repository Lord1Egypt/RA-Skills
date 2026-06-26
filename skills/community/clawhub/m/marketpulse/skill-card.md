## Description: <br>
Query real-time and historical financial data for equities, including prices, news, financial statements, metrics, analyst estimates, insider and institutional activity, SEC filings, earnings press releases, segmented revenues, stock screening, and macro interest rates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and finance-focused agents use Marketpulse to retrieve AIsa market data for stock research, watchlists, portfolio workflows, screening, SEC filing review, and macro interest-rate queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses AISA_API_KEY to send tickers, filters, dates, and similar financial research parameters to api.aisa.one. <br>
Mitigation: Install only when external transmission to AIsa is acceptable, avoid sensitive portfolio or client-specific screens unless approved, and scope the API key according to organizational policy. <br>
Risk: API requests may consume paid credits. <br>
Mitigation: Monitor usage, review command parameters before execution, and prefer narrower queries when testing or exploring data. <br>


## Reference(s): <br>
- [Marketpulse on ClawHub](https://clawhub.ai/aisadocs/marketpulse) <br>
- [AIsa API Reference](https://aisa.one/docs/api-reference/) <br>
- [AIsa](https://aisa.one) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python command examples; bundled CLI commands return JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; API calls send financial query parameters to AIsa endpoints and may consume paid credits.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
