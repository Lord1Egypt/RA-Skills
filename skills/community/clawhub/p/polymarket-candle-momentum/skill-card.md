## Description: <br>
Trade Polymarket 5-minute crypto fast markets using 1-minute Binance candle body analysis and volume surge detection across BTC, ETH, SOL, XRP, and BNB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mibayy](https://clawhub.ai/user/Mibayy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to inspect, configure, dry-run, or run a Python trading workflow for Polymarket fast markets using Binance candle and volume signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live cron mode can repeatedly place real-money trades without strong cumulative spending or loss controls. <br>
Mitigation: Start with dry-run, use a limited-purpose API key and small balance, and add or accept cumulative spend and loss limits before enabling live cron execution. <br>
Risk: The advertised win rate is not verified by the server evidence. <br>
Mitigation: Treat performance claims as unverified and independently backtest thresholds, assets, and fees before relying on the strategy. <br>
Risk: Position reporting may not be sufficient to confirm real exposure. <br>
Mitigation: Verify open positions directly in Simmer or Polymarket rather than relying only on the script's positions output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mibayy/polymarket-candle-momentum) <br>
- [Binance Klines API](https://api.binance.com/api/v3/klines) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code, shell commands, configuration notes, and text result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY for Simmer/Polymarket access; defaults to dry-run unless live trading is explicitly enabled.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release and clawhub.json; SKILL.md frontmatter says 1.6.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
