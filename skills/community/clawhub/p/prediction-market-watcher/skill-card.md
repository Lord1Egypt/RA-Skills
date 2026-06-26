## Description: <br>
Monitor, analyze, and trade on Kalshi and Polymarket prediction markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m-lwatcher](https://clawhub.ai/user/m-lwatcher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to review prediction-market positions, scan Kalshi markets for candidate opportunities, place Kalshi orders, and monitor settlement-related status. It also provides Polymarket read-only reference material for comparing active markets and prices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live Kalshi credentials can be used to place real-money bets automatically without a clear confirmation gate. <br>
Mitigation: Use demo or scan-only mode first, and run live automated betting only with explicit intent plus independent confirmation and spending controls. <br>
Risk: Kalshi private-key material is required for authenticated trading. <br>
Mitigation: Store the private key outside shared workspaces, restrict file permissions, and rotate credentials if exposure is suspected. <br>
Risk: Market scoring and settlement checks can be wrong or stale. <br>
Mitigation: Review the market rules, liquidity, current price source, and settlement basis before acting on recommendations. <br>


## Reference(s): <br>
- [Kalshi API Reference](references/kalshi-api.md) <br>
- [Polymarket API Reference](references/polymarket-api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/m-lwatcher/prediction-market-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call prediction-market APIs and may create local risk-state files when run by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
