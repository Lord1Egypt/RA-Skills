## Description:

Pans Churn Predictor analyzes customer usage trends, support tickets, contract status, and competitor activity to identify churn risk and generate retention suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Customer success, sales, and account teams use this skill to review AI compute customers for churn signals, inspect risk reasons, and prepare retention actions before renewal or escalation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The initialization command can overwrite existing local customer, usage, support ticket, and contract datasets.

Mitigation: Back up existing data before running --init, or run the skill against a separate test data directory when evaluating sample data.

Risk: Real customer and contract records may contain sensitive business information.

Mitigation: Use sanitized or authorized datasets and review access controls before installing or running the skill in a customer-success workflow.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dashiming/skills/pans-churn-predictor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with command-line examples and text risk reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces customer risk levels, detected churn signals, reason summaries, and retention suggestions.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
