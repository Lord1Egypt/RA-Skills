## Description: <br>
Trades post-count bin markets using a Poisson statistical model to predict the most likely bins based on historical posting rates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to evaluate Polymarket post-count bin markets with a Poisson cadence model and optionally execute trades through Simmer. It defaults to paper trading and requires an explicit live flag for real-money Polymarket execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real Polymarket trades when run in live mode with a live-capable Simmer API key. <br>
Mitigation: Run in paper mode first, provide live credentials only after review, and pass --live only when real-money trading risk is accepted. <br>
Risk: SIMMER_API_KEY is a sensitive credential with trading authority. <br>
Mitigation: Keep the key private, scope it appropriately, and avoid placing live-capable credentials in scheduled automation that is not fully controlled. <br>
Risk: The Poisson cadence model and threshold settings can produce incorrect trading signals under changing posting behavior or market conditions. <br>
Mitigation: Review model assumptions and tune position size, spread, volume, threshold, and open-position limits before enabling live execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/diagnostikon/polymarket-twitter-cadence-model-trader) <br>
- [Simmer skills homepage](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Console text with Simmer trade API calls and environment-based configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paper mode is the default; live trading requires SIMMER_API_KEY and the --live flag.] <br>

## Skill Version(s): <br>
0.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
