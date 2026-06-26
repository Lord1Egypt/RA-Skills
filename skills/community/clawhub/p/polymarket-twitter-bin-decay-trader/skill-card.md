## Description: <br>
Trades post-count prediction markets by tracking elapsed time to identify bins that are mathematically unreachable but still priced with residual probability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading automation operators use this skill to evaluate Polymarket post-count bin markets, generate paper-mode trades by default, and optionally execute live trades with explicit credentials and --live. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can execute real Polymarket trades using USDC when a live-capable SIMMER_API_KEY is present and --live is passed. <br>
Mitigation: Keep paper mode as the default, use a limited trading account for any live testing, and require explicit operator approval before enabling --live. <br>
Risk: The security evidence reports that some documented live-trading safety filters are incomplete. <br>
Mitigation: Audit simmer-sdk and verify the missing volume and date filters before relying on them for live risk controls. <br>
Risk: The skill requires a sensitive SIMMER_API_KEY credential. <br>
Mitigation: Store the key in a protected secret store, avoid live-capable credentials in automated environments, and rotate the key if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-twitter-bin-decay-trader) <br>
- [Simmer skills homepage](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Text logs, configuration values, and API trade requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live trading requires an explicit --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
