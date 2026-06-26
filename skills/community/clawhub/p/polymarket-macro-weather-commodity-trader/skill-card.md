## Description: <br>
Trades commodity markets based on extreme weather signals. When temperature markets show unusual readings (extreme heat or cold), it signals potential energy demand spikes or crop disruption that commodity markets have not yet priced in. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to scan weather prediction markets for extreme temperature signals, compare them with commodity prediction markets, and place simulated or explicitly enabled live Polymarket trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required SIMMER_API_KEY grants trading authority and should be treated as a high-value credential. <br>
Mitigation: Use revocable or least-privilege credentials where available and keep the key out of shared logs, prompts, and source control. <br>
Risk: Running with --live can place real Polymarket trades using USDC. <br>
Mitigation: Keep the default paper mode unless live trading is intentional, and set conservative max position, max open positions, spread, and minimum volume limits before live use. <br>
Risk: Weather-to-commodity signals can be indirect and may produce incorrect or stale trading assumptions. <br>
Mitigation: Review the strategy assumptions, market context, slippage warnings, and generated reasoning before allowing live execution. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/diagnostikon/polymarket-macro-weather-commodity-trader) <br>
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [Simmer SDK GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration, guidance] <br>
**Output Format:** [Text logs and configured trading actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trading requires the explicit --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
