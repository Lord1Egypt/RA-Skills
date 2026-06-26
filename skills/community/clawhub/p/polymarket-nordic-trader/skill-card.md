## Description: <br>
Trades Polymarket prediction markets focused on Scandinavian and Nordic events, including Swedish politics, Nordic business milestones, local weather extremes, and regional sports outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading-agent developers use this skill to discover Nordic-focused Polymarket markets, evaluate threshold-based trading signals, and place simulated or explicitly enabled live orders through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades with a provided API key. <br>
Mitigation: Run in simulated mode first, avoid --live until behavior is reviewed, and use a least-privilege or sandbox trading key where available. <br>
Risk: Automated trading may exceed the user's intended exposure if external controls are not configured. <br>
Mitigation: Set explicit position, loss, and open-position limits outside the skill before enabling live execution or scheduled runs. <br>
Risk: The required SIMMER_API_KEY is sensitive and may authorize trading actions. <br>
Mitigation: Keep the key private and do not place a live-capable key in environments where automated code can run with --live unintentionally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-nordic-trader) <br>
- [SMHI weather data](https://www.smhi.se/) <br>
- [Riksdagen open data](https://data.riksdagen.se/) <br>
- [Statistics Sweden](https://www.scb.se/) <br>
- [SVT Nyheter](https://www.svt.se/nyheter/) <br>
- [Dagens industri](https://www.di.se/) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk source](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Shell commands, Configuration] <br>
**Output Format:** [Console status text and trading API requests configured by environment variables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to simulated trading; live Polymarket orders require an explicit --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
