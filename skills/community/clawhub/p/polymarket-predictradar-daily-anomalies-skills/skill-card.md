## Description: <br>
Generates daily Polymarket anomaly reports for Black Swan probability shocks, Whale Wars opposing large bets, and Insider Watch new-wallet activity using live market data and real news context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnica](https://clawhub.ai/user/cnica) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, developers, and market researchers use this skill to scan Polymarket activity for unusual probability moves, opposing whale bets, and suspicious new-wallet trades. The generated report is intended as a research lead and verification aid, not trading advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnica/polymarket-predictradar-daily-anomalies-skills) <br>
- [Predictradar Polymarket data-layer examples](https://github.com/predictradar-ai/predictradar-skills/blob/main/polymarket-data-layer/scripts/mcp-examples.js) <br>
- [Polymarket Gamma API market metadata](https://gamma-api.polymarket.com/markets?condition_ids=<ID1>,<ID2>&limit=50) <br>
- [Predictradar MCP API endpoint](https://api.predictradar.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown daily report with linked markets, full wallet addresses, summary table, and optional JSON signal export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save wallet-linked public-market findings locally; users should verify the external data-layer dependency and treat anomaly labels as research leads rather than trading advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
