## Description: <br>
Complete trading workflows for Orderly Network DEX applications, from wallet connection through order execution, position management, and withdrawal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tarnadas](https://clawhub.ai/user/Tarnadas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to implement Orderly Network DEX trading flows, including wallet authentication, deposits, order placement, position monitoring, leverage handling, risk monitoring, and withdrawals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading workflows can move real funds or place market and limit orders. <br>
Mitigation: Add clear confirmations and previews, verify token and chain details, and enforce amount limits before enabling real transactions. <br>
Risk: Automated trading behavior can execute unintended or excessive trades. <br>
Mitigation: Provide controls to disable or restrict automation and test behavior on testnet or with small amounts before production use. <br>
Risk: Leverage and margin workflows can increase liquidation risk. <br>
Mitigation: Show leverage warnings, expose margin and risk indicators, and require user review before leverage changes or position-closing actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tarnadas/orderly-sdk-trading-workflows) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with TypeScript and TSX code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides workflow-oriented examples for Orderly SDK trading interfaces and automated trading bots.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
