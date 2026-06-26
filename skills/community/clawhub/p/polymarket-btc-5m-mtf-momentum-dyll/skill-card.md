## Description: <br>
Provides a BTC 5-minute Polymarket trading bot that aligns 1-minute, 3-minute, and 5-minute Binance BTC/USDT returns to generate directional momentum trades through Simmer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djdyll](https://clawhub.ai/user/djdyll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and developers use this skill to run or adapt a configurable BTC fast-market momentum strategy for Simmer-connected Polymarket trading. It can dry-run by default and can place live trades when explicitly configured and launched with live mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill with live trading enabled can place real trades and lose funds. <br>
Mitigation: Start in dry-run mode, keep trade size small, and use live mode only after validating configuration and strategy behavior. <br>
Risk: The skill requires a Simmer API key and may be scheduled to run repeatedly. <br>
Mitigation: Use the narrowest API key permissions available, store the key outside source files, and review cron or automaton settings before deployment. <br>
Risk: Momentum thresholds are intentionally configurable and may be unsuitable for a user's market conditions. <br>
Mitigation: Tune confidence, evaluation-window, and trade-size settings conservatively before increasing exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/djdyll/polymarket-btc-5m-mtf-momentum-dyll) <br>
- [Simmer API endpoint](https://api.simmer.markets) <br>
- [Binance Klines API endpoint](https://api.binance.com/api/v3/klines) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with Python scripts, shell commands, and JSON status output when automaton-managed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces trading signals, dry-run or live trade execution summaries, position status, and configurable environment-variable driven behavior.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
