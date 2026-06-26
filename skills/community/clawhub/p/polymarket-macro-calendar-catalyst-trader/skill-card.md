## Description: <br>
Trades Polymarket prediction markets that resolve near known calendar catalyst events such as FOMC meetings, tournament finals, geopolitical summits, crypto events, and space launches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and advanced trading operators use this skill to scan Polymarket markets for catalyst-adjacent opportunities, size positions with configured risk limits, and run in paper mode by default before any live trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SIMMER_API_KEY grants trading authority. <br>
Mitigation: Treat the key as a high-value credential, scope and rotate it where possible, and install the skill only when the operator accepts that authority. <br>
Risk: Live mode can place real Polymarket trades and create USDC losses. <br>
Mitigation: Start in paper mode, review position limits and strategy assumptions, and use --live only after accepting the financial risk. <br>
Risk: The strategy relies on static catalyst heuristics that may be stale or directionally wrong. <br>
Mitigation: Review the calendar, thresholds, and directional assumptions before live use, and tune limits conservatively. <br>


## Reference(s): <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Console text and configured trade orders via Simmer SDK] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live trading requires SIMMER_API_KEY and the --live flag.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
