## Description: <br>
Trades Polymarket prediction markets on social trend indicators, including loneliness indices, mental health policy, drug legalization, and cultural inflection points. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a configurable Polymarket social-trends trading strategy, starting in paper mode and optionally enabling live trading after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live Polymarket mode can place real USDC orders, and the release security summary says live-trading risk controls are weaker than the skill describes. <br>
Mitigation: Review before enabling live trading, start in paper mode, and use independent account-level limits in addition to the skill tunables. <br>
Risk: SIMMER_API_KEY is a sensitive trading credential. <br>
Mitigation: Use a dedicated, revocable key with limited funds and rotate or revoke it if exposure is suspected. <br>
Risk: Dependency behavior affects market discovery and order execution. <br>
Mitigation: Verify the simmer-sdk version before installation and deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-social-trends-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API Calls] <br>
**Output Format:** [Python script execution with console status logs and trade requests through simmer-sdk] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live trading requires the --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
