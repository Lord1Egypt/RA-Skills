## Description: <br>
Trades Polymarket prediction markets on sports championships, tournament outcomes, MVP awards, transfer windows, and season milestones using sports calendar, fan-bias, and probability-threshold signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to discover sports-related Polymarket markets, evaluate probability-extreme signals with sports-specific adjustments, and place paper trades by default or explicit live trades when configured. <br>

### Deployment Geography for Use: <br>
Global where prediction-market trading and Polymarket access are permitted <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place unattended real-money Polymarket trades when run in live mode with a funded credential. <br>
Mitigation: Keep the skill in paper mode until the code, position sizing, daily spend limits, market filters, and kill-switch rules are reviewed. <br>
Risk: SIMMER_API_KEY provides trading authority and should be treated as a financial credential. <br>
Mitigation: Store the key only in the intended runtime secret store, rotate it if exposed, and avoid sharing logs or configuration that reveal it. <br>
Risk: Prediction-market trading may be restricted by local laws or platform terms. <br>
Mitigation: Use live mode only after confirming local legal eligibility and platform access requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-sports-live-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>
- [ESPN sports scoreboard API](https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Console text with configurable environment variables and trading API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trades require an explicit --live flag and a SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
