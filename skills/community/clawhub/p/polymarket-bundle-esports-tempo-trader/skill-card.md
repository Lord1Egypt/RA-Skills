## Description: <br>
Trades tempo inconsistencies across Dota2 and esports game props on Polymarket. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators use this skill to identify and optionally trade inconsistencies among correlated Dota2 and esports tempo markets on Polymarket. It defaults to simulated trading and requires an explicit live flag before placing real-money orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money Polymarket trades and create financial loss. <br>
Mitigation: Start in paper mode, review position-size and trade-limit tunables, and use --live only when real-money trading risk is accepted. <br>
Risk: SIMMER_API_KEY grants trading authority and is a high-value credential. <br>
Mitigation: Protect SIMMER_API_KEY, avoid sharing it in logs or prompts, and rotate it if exposure is suspected. <br>
Risk: Market signals may be incomplete, stale, or wrong for active esports markets. <br>
Mitigation: Review detected opportunities, market volume, spreads, and position limits before enabling live execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/polymarket-bundle-esports-tempo-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Console text with Simmer SDK market discovery, analysis, and trade requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to simulated trades; live Polymarket orders require the --live flag and configured risk tunables.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
