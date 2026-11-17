## Description:

Trade prediction markets on Polymarket. Search markets, place orders, and manage positions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rachelbastian](https://clawhub.ai/user/rachelbastian)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search prediction markets, inspect market data, place or cancel Polymarket orders, manage positions, redeem settled positions, and configure trading strategies through the LuckyLobster API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live prediction-market trades and expose real money to loss.

Mitigation: Use it only with an account and budget you are willing to expose, check budget before trading, and prefer dry runs where supported.

Risk: Persistent autonomous and copy-trade strategies can place trades while the user is inactive.

Mitigation: Avoid enabling autonomous or copy-trade strategies unless their behavior is understood, set tight maxBudget limits, and monitor heartbeat and strategy status.

Risk: Token approvals, especially approve-all behavior, can expand wallet-level exposure.

Mitigation: Approve only the specific token type needed for the current action and review approval requests before submitting them.

## Reference(s):

- [LuckyLobster Homepage](https://luckylobster.io)
- [LuckyLobster ClawHub Skill Page](https://clawhub.ai/rachelbastian/skills/luckylobster-skill)
- [LuckyLobster Publisher Profile](https://clawhub.ai/user/rachelbastian)
- [LuckyLobster Agent API Base URL](https://luckylobster.io/api/agent/v1)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown guidance with HTTP and shell examples that return JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LUCKYLOBSTER_API_KEY; API calls can place live trades, cancel orders, approve tokens, manage positions, redeem settlements, and configure automated strategies.]

## Skill Version(s):

0.10.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
