## Description: <br>
Kalshi Weather Trader helps agents configure, dry-run, and optionally execute Kalshi weather-market trades using NOAA forecasts, the Simmer SDK, and DFlow on Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to inspect Kalshi weather positions, configure weather-trading thresholds and locations, and run dry-run or live automated temperature-market scans. Live trading requires Simmer API credentials and a Solana wallet private key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a raw Solana private key for live trading. <br>
Mitigation: Use a dedicated low-balance wallet, never reuse a primary wallet key, and store the key only in a secured environment. <br>
Risk: Live mode can place automated trades, and safeguards can be bypassed. <br>
Mitigation: Keep dry-run mode enabled until the strategy is understood, avoid --no-safeguards for live trades, and set explicit spending limits before enabling scheduled or quiet live runs. <br>
Risk: Weather temperature markets can resolve by gapping to near zero, so stop-loss monitoring may not cap losses. <br>
Mitigation: Size positions conservatively and assume each position can become a full loss. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/simmer/kalshi-weather-trader) <br>
- [Simmer API](https://api.simmer.markets) <br>
- [NOAA Weather API](https://api.weather.gov) <br>
- [DFlow Proof verification](https://dflow.net/proof) <br>
- [Simmer dashboard](https://simmer.markets/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, environment configuration, and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit JSON automaton status from the trading entrypoint; dry-run is the default unless live trading is explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
