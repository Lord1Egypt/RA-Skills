## Description: <br>
Trades cluster momentum continuation in 5-minute crypto Up/Down bundles on Polymarket. When 2+ coins (BTC, ETH, SOL, XRP) all show the same directional bias in one time slot, trades continuation on the next slot at micro sizes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to scan Polymarket 5-minute crypto Up/Down markets for cross-coin directional clusters and place micro-sized continuation trades. It defaults to simulated trading and requires an explicit live flag before placing real Polymarket orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running with --live can create real USDC exposure on Polymarket. <br>
Mitigation: Keep the default simulation mode until intentionally ready for live trading; review and set max position, minimum trade, and maximum open position tunables before using --live. <br>
Risk: SIMMER_API_KEY is a high-value credential with trading authority. <br>
Mitigation: Store it only in a secrets manager or protected runtime environment, limit access to trusted operators, and rotate it if exposed. <br>
Risk: The skill depends on the third-party simmer-sdk package for market access and trade execution. <br>
Mitigation: Review the dependency and pin an approved version before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-micro-cluster-momentum-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Console logs and Simmer SDK trade requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to simulation mode unless run with --live.] <br>

## Skill Version(s): <br>
0.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
