## Description: <br>
Prediction Market Trader helps agents analyze Kalshi prediction markets by authenticating to the API, scanning markets, de-vigging Sofascore odds, calculating probabilities, sizing positions, and preparing or executing order actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[merjua14](https://clawhub.ai/user/merjua14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to evaluate prediction-market opportunities, compare Kalshi prices with de-vigged odds, apply Kelly-style sizing, and manage trading risk. It is intended for workflows where a human reviews market data and approves any account action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use real Kalshi account credentials to place or cancel live orders. <br>
Mitigation: Require explicit human approval before every order or cancellation and use the skill only with accounts intended for this workflow. <br>
Risk: Kalshi private keys are highly sensitive and may authorize account actions. <br>
Mitigation: Store credentials in environment variables or a secrets manager, avoid logging keys, and rotate credentials if exposure is suspected. <br>
Risk: The documented dry-run workflow depends on a trading script that is not present in the artifact. <br>
Mitigation: Do not rely on dry-run behavior unless the missing script is supplied, reviewed, and tested before use. <br>
Risk: Automated market matching or stale odds can produce incorrect trade decisions. <br>
Mitigation: Verify event matches by name, re-check current odds immediately before action, and document source data and edge calculations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/merjua14/prediction-market-trader) <br>
- [Lessons Learned](references/lessons-learned.md) <br>
- [Kalshi Market Categories & Series Tickers](references/market-categories.md) <br>
- [Risk Management Rules](references/risk-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe API calls and trade-sizing calculations; any live trading action should require human approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
