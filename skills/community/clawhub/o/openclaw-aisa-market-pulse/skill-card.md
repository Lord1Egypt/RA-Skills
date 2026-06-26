## Description: <br>
Query real-time and historical financial data across equities and crypto - prices, market moves, metrics, and trends for analysis, alerts, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaimengphp](https://clawhub.ai/user/chaimengphp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use MarketPulse to retrieve stock and cryptocurrency market data for portfolio analysis, investment research, screening, alerts, and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends API keys and requested market queries to AIsa. <br>
Mitigation: Use a dedicated or least-privilege AISA_API_KEY and install only when the AIsa service is trusted for the intended queries. <br>
Risk: Market queries may reveal confidential watchlists or proprietary screening criteria. <br>
Mitigation: Avoid submitting sensitive watchlists or proprietary criteria unless approved for the deployment environment. <br>
Risk: API calls can consume paid credits or quota. <br>
Mitigation: Monitor AIsa usage, costs, and remaining credits when running automated analysis or repeated polling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chaimengphp/openclaw-aisa-market-pulse) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AIsa API reference](https://docs.aisa.one/reference/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, curl, and AISA_API_KEY; sends market-data queries to the AIsa API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
