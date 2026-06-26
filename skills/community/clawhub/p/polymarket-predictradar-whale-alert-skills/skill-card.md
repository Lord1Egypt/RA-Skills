## Description: <br>
Polymarket Whale Alert monitors the past 24 hours of large Polymarket orders from smart-money HUMAN, MM, and SIGNAL profiles and returns structured whale-trade reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnica](https://clawhub.ai/user/cnica) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to ask for Polymarket whale alerts, identify large smart-money buys and sells, and inspect linked markets, wallet addresses, order sizes, win rates, and PnL signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries a live/shared Polymarket data layer and wallet-level analytics, which can expose privacy-transparency and data-quality concerns. <br>
Mitigation: Use it only when wallet-level Polymarket analytics are desired, and verify important reports against the linked market and profile sources before relying on them. <br>
Risk: Unclassified results, stale smart-money classifications, or degraded PnL thresholds may make reported whale activity less reliable. <br>
Mitigation: Treat lowered-threshold or unclassified output as lower confidence and review the stated filters, threshold, and classification status in the generated report. <br>
Risk: The report depends on referenced polymarket-data-layer helpers and live data availability. <br>
Mitigation: Confirm the referenced helpers and data service are available and trustworthy in the deployment environment before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnica/polymarket-predictradar-whale-alert-skills) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/cnica) <br>
- [Predictradar Polymarket data layer MCP examples](https://github.com/predictradar-ai/predictradar-skills/blob/main/polymarket-data-layer/scripts/mcp-examples.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with linked wallet addresses, linked Polymarket markets, tabular trade details, and summary headers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are generated from live read-only Polymarket analytics queries for a recent time window; reliability depends on the shared data layer and classification freshness.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
