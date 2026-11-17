## Description:

Create a Gougoubi proposal condition from minimal input with deterministic defaults for deadline, trade deadline, normalization, and transaction submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when a Gougoubi proposal already exists and they need to add a condition from a proposal identifier and condition name. It prepares deterministic deadline, trade-deadline, normalization, and transaction fields while preserving wallet confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A condition transaction could be submitted with an unintended proposal address, condition name, deadline, trade deadline, or normalization flag.

Mitigation: Review the generated condition details and wallet prompt before signing.

Risk: The skill prepares transaction data for a wallet action.

Mitigation: Keep wallet confirmation in the flow; the evidence does not show automatic wallet bypass.

## Reference(s):

- [Gougoubi Premarket Proposals](https://gougoubi.ai/premarket/proposals)
- [ClawHub Skill Page](https://clawhub.ai/chinasong/skills/gougoubi-create-condition)
- [Publisher Profile](https://clawhub.ai/user/chinasong)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON response with normalized input, transaction status, warnings, or failure details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a transaction hash after user-confirmed submission; defaults are deterministic and reflected in the normalized payload.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
