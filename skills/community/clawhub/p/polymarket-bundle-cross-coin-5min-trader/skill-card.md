## Description: <br>
Trades cross-coin divergence in 5-minute crypto Up/Down bundles on Polymarket, sizing simulated or live orders by divergence magnitude and configured risk limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill as an automated Polymarket trading template for detecting cross-coin divergence across BTC, ETH, SOL, and XRP 5-minute Up/Down markets. It defaults to paper trading and requires an explicit live flag before placing real USDC trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running with --live can place real Polymarket USDC trades. <br>
Mitigation: Keep the skill in paper mode until tested, then use --live only after reviewing position limits, thresholds, and current market behavior. <br>
Risk: SIMMER_API_KEY grants trading authority and is a sensitive credential. <br>
Mitigation: Use the least-privileged or sandbox trading credential available and store it only in the intended runtime secret mechanism. <br>
Risk: Automated trading decisions may be wrong when correlation assumptions fail or market liquidity changes. <br>
Mitigation: Review and tune max position size, maximum open positions, spread limits, minimum volume, and deviation thresholds before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-bundle-cross-coin-5min-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Console log text with Simmer SDK trading API calls controlled by environment configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to simulated trading; live Polymarket trading requires --live and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
