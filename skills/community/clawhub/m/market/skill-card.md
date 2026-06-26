## Description: <br>
Query real-time and historical financial data across equities and crypto--prices, market moves, metrics, and trends for analysis, alerts, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query AIsa market data for equities, cryptocurrencies, financial statements, SEC filings, analyst estimates, screening, alerts, and portfolio reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive AISA_API_KEY credential to call the AIsa financial-data API. <br>
Mitigation: Use a dedicated, revocable API key and avoid sharing production or broadly privileged credentials with automated workflows. <br>
Risk: API calls may consume paid credits. <br>
Mitigation: Confirm the requester trusts AIsa and use an account or key with limited balance where possible. <br>
Risk: Market, financial, and crypto data can be incomplete, delayed, or unsuitable as the sole basis for decisions. <br>
Mitigation: Treat returned data as analysis input and verify important financial conclusions against authoritative sources before acting. <br>


## Reference(s): <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>
- [AIsa](https://aisa.one) <br>
- [ClawHub Market Skill](https://clawhub.ai/bibaofeng/market) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; API responses may include usage cost and remaining credits.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
