## Description: <br>
Trade Polymarket BTC 5-minute fast markets with a paper-first, magnitude-gated conviction-ladder strategy that uses Binance 1-minute momentum and explicitly treats prior performance claims as retracted. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and traders use this skill to run or adapt a paper-first Polymarket BTC 5-minute fast-market strategy with configurable magnitude gates, tiered position sizing, and budget caps. It is intended as an unvalidated reference framework, not as financial advice or a proven trading edge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades and change account state. <br>
Mitigation: Run paper mode first, keep the default budget and per-market caps until independently validated, and enable live mode only after reviewing the wallet and credential setup. <br>
Risk: The skill requires sensitive Simmer or wallet credentials. <br>
Mitigation: Store SIMMER_API_KEY and any wallet private key outside source files, restrict access to the runtime environment, and avoid using an external wallet key unless self-custody trading is required. <br>
Risk: The documented performance claim was retracted and the magnitude gate is not a validated profitable edge. <br>
Mitigation: Do not rely on historical win-rate claims; run paper validation under current market conditions and treat parameter increases as increased exposure rather than increased expected return. <br>
Risk: Automated runs can redeem resolved positions and cancel attributed GTC orders. <br>
Mitigation: Review order attribution and cleanup behavior before cron or live operation, and monitor early live runs for unexpected account changes. <br>
Risk: Stop-loss and take-profit monitoring may not fire before 5-minute markets resolve. <br>
Mitigation: Use conservative position sizing and budget caps as the primary risk controls for sub-15-minute markets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simmer/polymarket-fast-scaler) <br>
- [Publisher profile](https://clawhub.ai/user/simmer) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Disclaimer](artifact/DISCLAIMER.md) <br>
- [Paper validation results](artifact/paper-validation-results.md) <br>
- [Polymarket trading fees](https://docs.polymarket.com/trading/fees) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code, shell commands, configuration values, and JSON status reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paper mode is the default; live mode can place real trades when explicitly enabled.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
