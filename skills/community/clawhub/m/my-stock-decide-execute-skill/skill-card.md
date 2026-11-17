## Description:

Orchestrates a stock trading workflow that runs decision analysis, places a Longbridge brokerage order, and records the result only when the user explicitly requests trading decision and execution or names the skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canonxu](https://clawhub.ai/user/canonxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to coordinate an end-to-end securities workflow from trading decision analysis through live order placement and operational logging. It is intended for explicit trading execution requests, not general market discussion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can proceed to live Longbridge brokerage orders without a separate final user approval step.

Mitigation: Require final confirmation immediately before order placement, use a dry-run default, and enforce order-size limits before connecting a live account.

Risk: Incorrect or incomplete extracted trading parameters could result in unintended order details.

Mitigation: Validate symbol, side, price, and quantity before execution, and stop the workflow if any required value is missing or invalid.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/canonxu/skills/my-stock-decide-execute-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown status report with decision details, order result, and log summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stock symbol, buy or sell direction, target price, target position or share count, order status, order ID or failure reason, and log record count.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
