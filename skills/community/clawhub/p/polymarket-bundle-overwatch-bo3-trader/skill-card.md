## Description: <br>
Detects and can trade pricing gaps between Overwatch best-of-3 series winner markets and individual game winner markets on Polymarket. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading agents use this skill to monitor Overwatch BO3 Polymarket bundles, compare implied series probabilities with quoted series prices, and submit paper or explicitly enabled live trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades using USDC. <br>
Mitigation: Run in the default paper mode first and use live mode only with the explicit --live flag after reviewing position limits. <br>
Risk: SIMMER_API_KEY is a high-value trading credential. <br>
Mitigation: Store the credential securely, avoid logging it, and limit access to agents that are intended to trade. <br>
Risk: The trading strategy should not be treated as guaranteed or risk-free, especially when no Game 3 market is available. <br>
Mitigation: Review the signal before live use, keep conservative tunables, and adjust the minimum violation, position size, and market filters for the user's risk tolerance. <br>
Risk: Thin markets, spreads, slippage, and short time to resolution can degrade execution quality. <br>
Mitigation: Use the configured minimum volume, maximum spread, slippage, days-to-resolution, and maximum open-position controls before submitting live trades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-bundle-overwatch-bo3-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration] <br>
**Output Format:** [Console logs and Simmer trade requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trades require an explicit --live flag.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
