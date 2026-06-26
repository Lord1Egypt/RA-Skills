## Description: <br>
Trades 2nd and 3rd order effects from nearly-resolved Polymarket events by identifying cascade chains and trading lagging downstream markets before they fully reprice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading agents use this skill to scan Polymarket-style event markets, classify near-resolution trigger events, map expected macro cascades, and place paper or explicitly enabled live trades with configurable risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated trading can create real financial losses when live mode is enabled. <br>
Mitigation: Use paper mode first, keep withdrawals disabled, verify risk limits, and require explicit approval before any live strategy or order. <br>
Risk: The required API key grants trading authority. <br>
Mitigation: Provide only trading-permission credentials, store them as sensitive secrets, and avoid keys with withdrawal capability. <br>
Risk: Cascade signals can be wrong or stale during fast-moving macro events. <br>
Mitigation: Review configured thresholds, spread and position limits, and use additional market or news confirmation before live execution. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/diagnostikon/polymarket-macro-event-cascade-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with trade status messages and configuration-driven trading actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless live trading is explicitly enabled.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
