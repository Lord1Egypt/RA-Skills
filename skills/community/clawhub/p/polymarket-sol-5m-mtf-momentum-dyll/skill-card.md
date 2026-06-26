## Description: <br>
Runs a SOL 5-minute multi-timeframe momentum trading workflow that uses Binance SOL/USDT returns to identify Simmer/Polymarket fast-market trade opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djdyll](https://clawhub.ai/user/djdyll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and agent operators use this skill to configure, dry-run, and optionally execute an automated SOL 5-minute momentum strategy. It is intended for users who can review trading logic, tune thresholds, and control live execution risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live trading can spend real funds or simulated balances when --live or managed automation is enabled. <br>
Mitigation: Run in dry-run mode first, keep trade size constrained, and only enable --live after reviewing the strategy, venue, API key scope, and current configuration. <br>
Risk: The release mixes SOL, BTC, Polymarket, and Simmer wording, which could cause confusion about the intended asset or execution venue. <br>
Mitigation: Confirm the intended asset, market venue, and API environment before enabling cron automation or live execution. <br>
Risk: Automated minute-by-minute execution can repeatedly evaluate markets and place trades if thresholds are met. <br>
Mitigation: Keep automation disabled until reviewed, retain conservative max-trades and trade-size settings, and monitor positions with the provided status command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/djdyll/polymarket-sol-5m-mtf-momentum-dyll) <br>
- [Simmer API endpoint](https://api.simmer.markets) <br>
- [Binance Klines API endpoint](https://api.binance.com/api/v3/klines) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell commands; runtime output is plain text with optional JSON automaton status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; default command mode is dry run, while --live can execute trades.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
