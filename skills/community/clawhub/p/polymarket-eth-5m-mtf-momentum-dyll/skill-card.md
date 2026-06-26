## Description: <br>
Runs a multi-timeframe ETH/USDT momentum strategy that can place simulated or live trades on Polymarket five-minute fast markets through Simmer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djdyll](https://clawhub.ai/user/djdyll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and agent operators use this skill as a configurable automated trading template for testing and running ETH five-minute momentum strategies on Simmer/Polymarket fast markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary identifies a BTC/ETH mismatch and a live-trading path that could cause unintended trades. <br>
Mitigation: Verify the intended asset and market before use, run in paper mode first, and enable live mode only after adding limits, confirmation, and monitoring. <br>
Risk: The skill requires SIMMER_API_KEY and supports configurable SIMMER_API_URL and TRADING_VENUE values. <br>
Mitigation: Limit and monitor the API key, and avoid untrusted API URLs or trading venues. <br>
Risk: Cron or managed automaton execution can repeatedly evaluate markets and attempt trades. <br>
Mitigation: Enable scheduled or managed execution only after validating thresholds, trade size, max trades per run, and operational alerts. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/djdyll/polymarket-eth-5m-mtf-momentum-dyll) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/djdyll) <br>
- [Simmer Markets API endpoint](https://api.simmer.markets) <br>
- [Binance kline API endpoint](https://api.binance.com/api/v3/klines) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API Calls, JSON] <br>
**Output Format:** [CLI text with optional JSON automaton status reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; dry run is the default, and live trading requires --live.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
