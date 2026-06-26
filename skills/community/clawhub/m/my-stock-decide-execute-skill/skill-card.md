## Description: <br>
Orchestrates an explicit stock-trading workflow that generates a trade decision, submits a Longbridge brokerage order, and archives the operation log. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canonxu](https://clawhub.ai/user/canonxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill when they explicitly want an agent to run an end-to-end stock trading workflow: decide on an action, place a live brokerage order, and record the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to place live brokerage orders, but the security evidence says it does not require a hard final confirmation with exact order details before live execution. <br>
Mitigation: Require explicit confirmation of ticker, side, order type, price, quantity, account, and maximum exposure immediately before submitting any order; use paper trading or dry-run mode first. <br>
Risk: Incorrect decision extraction or incomplete parameter validation could submit an unintended order. <br>
Mitigation: Validate all trading parameters against strict price, size, and order-type limits before invoking the Longbridge trading skill, and terminate the workflow if any required value is missing. <br>
Risk: Trade logs may contain sensitive account, order, or strategy information. <br>
Mitigation: Confirm where trade logs are stored, restrict access to authorized users, and avoid recording unnecessary secrets or credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/canonxu/my-stock-decide-execute-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown or plain text status messages with trade parameters, order results, and log summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ticker, side, target price, target position or share count, order status, order identifier, failure reason, and log summary.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
