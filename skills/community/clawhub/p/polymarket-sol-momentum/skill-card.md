## Description: <br>
Trades Polymarket crypto prediction markets for Solana, Bitcoin, and Ethereum using CoinGecko momentum signals, with Simmer context checks for flip-flop detection and slippage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chokle](https://clawhub.ai/user/chokle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to scan crypto prediction markets, compare market prices against CoinGecko momentum signals, and place simulated or live trades through Simmer when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The strategy can run scheduled live trades with real funds through a Simmer-connected venue. <br>
Mitigation: Start with TRADING_VENUE=sim, keep TRADE_AMOUNT_USD and MAX_TRADES_PER_RUN low, and enable live venues only after reviewing account limits and accepting loss risk. <br>
Risk: Automated market selection can act on weak, stale, or misleading momentum signals. <br>
Mitigation: Review the signal source and thresholds before deployment, monitor dry-run behavior, and customize the strategy for the intended market conditions. <br>
Risk: A live-capable API key permits recurring automated trading from the configured environment. <br>
Mitigation: Protect SIMMER_API_KEY, scope account permissions where possible, and do not provide live-capable credentials unless live trading is intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chokle/polymarket-sol-momentum) <br>
- [Simmer Docs](https://docs.simmer.markets) <br>
- [Simmer Skill Building Guide](https://docs.simmer.markets/skills/building) <br>
- [CoinGecko Free API](https://www.coingecko.com/en/api/documentation) <br>
- [Polymarket](https://polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Code, API calls] <br>
**Output Format:** [Markdown guidance with Python code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and can run on a cron schedule; live trading requires explicit live configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
