## Description:

Power Oracle helps agents compute workout work and power from structured or shorthand workout details through the WorkCapacity API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workcapacity-io](https://clawhub.ai/user/workcapacity-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to validate workout movement inputs, call Power Oracle, and report authoritative workout work or power results. It is not intended for coaching, programming, nutrition, injury, recovery, or general fitness advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send workout details and body metrics to WorkCapacity.

Mitigation: Use the skill only when the user is comfortable sharing the required workout and body-metric inputs with WorkCapacity, and avoid collecting unnecessary personal data.

Risk: The compute endpoint may require an x402 payment proof.

Mitigation: Require explicit user confirmation before generating or submitting any x402 payment proof, and retry only the exact validated compute request.

## Reference(s):

- [API Contract](references/api-contract.md)
- [Power Oracle Documentation](https://www.workcapacity.io/docs/power-oracle)
- [ClawHub Skill Page](https://clawhub.ai/workcapacity-io/skills/power-oracle)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain-text summaries with API request details when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Power Oracle session work, elapsed average power, split-level observations, notes, and payment-challenge handling guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
