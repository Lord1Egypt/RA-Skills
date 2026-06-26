## Description: <br>
Trades mean-reversion on crypto 5-minute interval markets after detecting a single extreme probability pulse (p > 70% or p < 30%) on Polymarket. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to run a configurable micro-trading strategy for Polymarket crypto interval markets. It discovers short-duration markets, detects extreme probability pulses, and places paper trades by default or live trades only when explicitly launched with the live flag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires SIMMER_API_KEY, which grants trading authority. <br>
Mitigation: Protect the key as a financial credential and install only when you trust Simmer, simmer-sdk, and the publisher. <br>
Risk: Live mode can place real Polymarket orders using USDC. <br>
Mitigation: Use the default paper mode while reviewing behavior and limits; run with --live only when real orders are intentional. <br>
Risk: Automated trading can exceed the user's intended exposure if limits are misconfigured. <br>
Mitigation: Review and set the provided position, spread, volume, threshold, and maximum-open-position tunables before enabling live trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-micro-pulse-revert-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk source](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Console text from a Python trading script, with environment-based configuration and Simmer SDK trade calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require the explicit --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0 and clawhub.json lists 0.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
