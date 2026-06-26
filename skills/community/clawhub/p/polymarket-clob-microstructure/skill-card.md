## Description: <br>
Analyzes Polymarket CLOB order book microstructure to find structural inefficiencies, score active markets, generate trading signals, and optionally trade mean-reversion signals through Simmer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mibayy](https://clawhub.ai/user/Mibayy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading automation operators use this skill to scan active Polymarket markets for order-book microstructure signals and evaluate whether fake-breakout mean-reversion trades meet configured limits. The skill defaults to dry-run mode and requires an explicit live flag before placing trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place repeated real-money trades through scheduled execution. <br>
Mitigation: Run in dry-run first, enable live mode only intentionally, set conservative trade-size and max-trades limits, and monitor exposure and losses. <br>
Risk: The skill requires a Simmer API key for market access and trading. <br>
Mitigation: Use the least-privileged Simmer key available, store it only as an environment variable, and rotate or revoke it if the runtime is shared or compromised. <br>
Risk: External market data, order-book depth, and signal quality can be stale, incomplete, or unsuitable for the user's trading objectives. <br>
Mitigation: Review generated signals before live use, keep slippage and context checks enabled, and do not rely on the scanner without independent exposure and monitoring controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mibayy/polymarket-clob-microstructure) <br>
- [Polymarket CLOB order book endpoint](https://clob.polymarket.com/book) <br>
- [Polymarket trades data endpoint](https://data-api.polymarket.com/trades) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Analysis, Shell commands, Configuration] <br>
**Output Format:** [Console logs, trading signal summaries, and dry-run or live execution summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a managed automaton every five minutes; dry-run is the default, while live mode can place configured Simmer trades.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
