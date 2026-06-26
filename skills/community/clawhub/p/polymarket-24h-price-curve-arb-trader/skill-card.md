## Description: <br>
Trades structural mispricings in crypto price-threshold markets by reconstructing the implied probability distribution curve across multiple strike levels and detecting mathematical violations such as monotonicity breaks and range-sum inconsistencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and agent developers use this skill to scan Polymarket crypto price-threshold markets, identify implied-CDF inconsistencies, and run paper trades by default or live trades only when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can use real-money Polymarket trading access. <br>
Mitigation: Use paper mode first, enable live trading only intentionally, and provide a restricted low-balance API key. <br>
Risk: SIMMER_API_KEY is a high-value credential with trading authority. <br>
Mitigation: Store the key as a secret, avoid sharing it in prompts or logs, and rotate or revoke it after use. <br>
Risk: Trading behavior depends on external market data, simmer-sdk behavior, and risk tunables. <br>
Mitigation: Review the simmer-sdk dependency and verify tunables such as SIMMER_MIN_VIOLATION, max position size, and spread limits before live trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-24h-price-curve-arb-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk source repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Console logs, command-line execution, tunable configuration, and trading API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require explicit live mode and valid trading credentials.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
