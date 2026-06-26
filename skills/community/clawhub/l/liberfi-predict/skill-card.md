## Description: <br>
Browse prediction market events, manage positions, and place orders on Kalshi and Polymarket using the LiberFi CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bombmod](https://clawhub.ai/user/bombmod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to browse Kalshi and Polymarket prediction markets, inspect balances, positions, trades, and orders, and prepare or submit prediction-market orders through the LiberFi CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can help place real prediction-market orders and interact with balances, deposits, approvals, and cancellations. <br>
Mitigation: Require explicit user approval before installation, login, wallet setup, deposits, approvals, or trades, and keep limited funds in wallets used with the skill. <br>
Risk: The release relies on the LiberFi CLI and server-managed wallet signing for prediction-market account access. <br>
Mitigation: Install and use it only when the user trusts LiberFi with this access, and avoid exposing or logging sensitive credentials or account details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bombmod/liberfi-predict) <br>
- [LiberFi homepage](https://liberfi.io) <br>
- [Prediction order flow reference](reference/order-flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON-oriented command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses LiberFi CLI commands with --json for structured responses; trade execution should wait for explicit user confirmation.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
