## Description:

Process payments for ecommerce operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and ecommerce operators use this skill to configure and invoke payment-processing workflows that return JSON processing results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment operations are high-impact and the skill is under-specified about charge, refund, and account authorization.

Mitigation: Require explicit user authorization before any charge, refund, or account action, and confirm the amount, merchant, payment token, and operation before execution.

Risk: The skill asks for an API key without documented safeguards.

Mitigation: Use least-privilege test credentials first, keep PROCESS_API_KEY in a secret manager or environment variable, and avoid logging secrets.

Risk: Raw payment data could be mishandled if card details pass through generic input or output files.

Mitigation: Use documented compliant tokenization flows and avoid storing or routing raw card data through logs or generic files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-payment-processor)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON]

**Output Format:** [Markdown with bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PROCESS_API_KEY configuration before use.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
