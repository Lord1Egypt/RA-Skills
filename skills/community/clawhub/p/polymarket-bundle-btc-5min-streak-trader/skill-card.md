## Description: <br>
Trades BTC Up or Down 5-minute Polymarket intervals by detecting same-direction streaks and placing mean-reversion trades on the next interval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators use this skill to run or adapt a Simmer-based BTC 5-minute Polymarket streak strategy with configurable position, spread, volume, and threshold controls. It defaults to paper trading and requires explicit live-mode enablement for real USDC trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real-money live or cron trading can use a sensitive Simmer API key without tightly scoped release-level limits. <br>
Mitigation: Start in paper mode, use a least-privilege Simmer key if available, and do not enable --live or cron mode until trade size, total daily spend, allowed markets, and emergency stop controls are explicit. <br>
Risk: The trading strategy depends on market discovery, interval parsing, and short-horizon mean-reversion assumptions that can fail in changing market conditions. <br>
Mitigation: Review candidate markets and signal output before live execution, and keep max position, max open positions, spread, volume, and threshold tunables conservative. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/diagnostikon/polymarket-bundle-btc-5min-streak-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Console logs, configured trading actions, and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; paper trading is the default, while live Polymarket execution requires the --live flag.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
