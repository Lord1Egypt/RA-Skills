## Description: <br>
Systematically finds low-probability Polymarket longshot markets and scores them with cross-category macro signals before optionally placing paper or live trades through Simmer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading agents use this skill to scan prediction markets for asymmetric longshot opportunities, score macro support, and execute simulated trades by default. Users may opt into live Polymarket trading only when they explicitly run the skill in live mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money Polymarket trades. <br>
Mitigation: Start in paper mode, review the tunable limits, and use live mode only when intentionally connecting a funded trading account. <br>
Risk: The skill requires SIMMER_API_KEY, a sensitive trading credential. <br>
Mitigation: Use a dedicated revocable API key with limited funds or permissions where possible. <br>
Risk: The unpinned simmer-sdk dependency is part of the runtime trust boundary. <br>
Mitigation: Review and trust the dependency before installation or live trading use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-macro-asymmetric-longshot-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Terminal logs, Simmer trade API calls, and configurable environment-based risk parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live trading requires an explicit --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
