## Description: <br>
Predicts short-term BTC market direction using multi-timeframe market data, funding rates, sentiment, and liquidity signals to recommend execute, watch, or no-trade outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maserati8](https://clawhub.ai/user/maserati8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and trading operators use this skill as decision support for BTC short-term trend analysis on OKX-style futures workflows. It converts market structure, position, sentiment, liquidity, and trigger checks into a structured signal that still requires independent human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat BTC trading recommendations as permission to trade real money. <br>
Mitigation: Treat execute signals as informational decision support, verify them independently, and require explicit human approval plus separate risk controls before any trade. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/maserati8/okxprediction) <br>
- [Logic reference](references/logic.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Structured JSON signal with explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes direction, score, signal, entry type, stop loss, target, and rationale when sufficient input data is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
