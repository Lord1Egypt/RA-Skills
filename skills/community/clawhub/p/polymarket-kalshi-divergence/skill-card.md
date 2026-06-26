## Description: <br>
Cross-platform arbitrage between Kalshi and Polymarket that monitors 13 Kalshi event series and compares prices to equivalent Polymarket markets, generating BUY signals above an 8% divergence and SELL signals above a 10% divergence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mibayy](https://clawhub.ai/user/Mibayy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this managed automaton to scan Kalshi and Polymarket prediction markets for cross-platform price divergences, inspect generated trade signals, and optionally execute Polymarket trades through SimmerClient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place automated financial trades. <br>
Mitigation: Use dry-run and the default simulated venue first; enable --live or a real trading venue only after accepting the financial risk. <br>
Risk: The managed automaton is scheduled every five minutes and can repeatedly scan or trade. <br>
Mitigation: Monitor the schedule, disable it when scans or trades are no longer desired, and keep KALSHI_TRADE_SIZE and divergence thresholds conservative. <br>
Risk: Cross-market matching is keyword and score based, so a Kalshi market can be paired with an imperfect Polymarket match. <br>
Mitigation: Review signal logs before live use and rely on the built-in context checks for severe flip-flop warnings, high slippage, or low edge. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mibayy/polymarket-kalshi-divergence) <br>
- [Kalshi Trade API endpoint](https://api.elections.kalshi.com/trade-api/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Console text and logs with trade-signal details, plus optional SimmerClient trade API requests in live mode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run is the default; live trading requires --live and a configured SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
2.0.5 (source: server release evidence, SKILL.md frontmatter, clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
