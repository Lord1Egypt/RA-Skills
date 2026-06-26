## Description: <br>
Trade prediction markets on Polymarket. Search markets, place orders, and manage positions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rachelbastian](https://clawhub.ai/user/rachelbastian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use Lucky Lobster to search Polymarket markets, inspect prices and positions, place or cancel orders, close positions, and redeem settled markets through the LuckyLobster API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent persistent authority to place trades, cancel orders, close positions, and redeem settled markets. <br>
Mitigation: Require explicit user approval for every wallet-affecting action, keep balances and budgets limited, and review order details before execution. <br>
Risk: The LuckyLobster API key grants ongoing account access if stored or exposed incorrectly. <br>
Mitigation: Store the key only in approved agent configuration or environment storage, avoid committing env files, and rotate or revoke the key if exposure is suspected. <br>


## Reference(s): <br>
- [LuckyLobster homepage](https://luckylobster.io) <br>
- [ClawHub skill page](https://clawhub.ai/rachelbastian/lucky-lobster) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with HTTP, JSON, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LUCKYLOBSTER_API_KEY for authenticated LuckyLobster API access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
