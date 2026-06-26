## Description: <br>
Autonomous BTC-USDC trading bot for Hyperliquid mainnet using a multi-timeframe anchored VWAP strategy with live execution controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidm413](https://clawhub.ai/user/davidm413) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to configure and run an autonomous BTC-USDC trading loop on Hyperliquid mainnet. It is intended for live market execution and status review, so users should validate controls before connecting funds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trade real funds continuously on Hyperliquid mainnet using a private key. <br>
Mitigation: Use only a dedicated low-balance wallet, add a dry-run or testnet mode, and require explicit live-trading confirmation before any mainnet execution. <br>
Risk: Safety controls may be overstated relative to the implemented behavior. <br>
Mitigation: Test hard caps, stop-loss and take-profit handling, daily-loss accounting, and the kill switch before connecting funded accounts. <br>
Risk: Losses can occur quickly because the release describes leveraged autonomous crypto trading. <br>
Mitigation: Keep position and daily-loss limits conservative, monitor the first sessions manually, and stop trading immediately if observed behavior differs from expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidm413/hyperliquid-btc-auto-trader) <br>
- [Publisher profile](https://clawhub.ai/user/davidm413) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown and text responses with shell commands and Python-based trading actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Hyperliquid wallet environment variables and can initiate continuous mainnet trading when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
