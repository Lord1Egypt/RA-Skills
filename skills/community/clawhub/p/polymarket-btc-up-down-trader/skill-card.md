## Description: <br>
Trade Polymarket BTC daily and weekly UP/DOWN markets with empirically-anchored exit discipline. Enters on CEX momentum divergence; exits automatically on time cap, volume spike, or target capture. Use when the user wants to trade BTC direction markets (hours/days duration), not fast 5-minute markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators use this skill to run a Polymarket BTC daily or weekly UP/DOWN trading workflow with dry-run support, configurable position limits, and automated exit checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades with financial loss exposure. <br>
Mitigation: Start in dry-run mode, use small position and daily budget limits, and understand the strategy before enabling --live. <br>
Risk: Wallet private keys and API keys are sensitive credentials. <br>
Mitigation: Use managed wallets or a minimally funded dedicated wallet where possible, and keep private keys out of logs and chat. <br>
Risk: Prediction-market trades and on-chain orders may be irreversible or affected by market, resolution, and operator risks. <br>
Mitigation: Review the disclaimer, monitor positions, and keep conservative exit, position, and budget settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simmer/polymarket-btc-up-down-trader) <br>
- [Publisher profile](https://clawhub.ai/user/simmer) <br>
- [DISCLAIMER.md](artifact/DISCLAIMER.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with CLI commands, Python strategy execution, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in dry-run mode by default or live mode when configured with API and wallet credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
