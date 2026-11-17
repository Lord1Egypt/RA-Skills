## Description:

Calculates tiered GPU compute quotes using customer scale, contract duration, and prepayment discounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, finance, and operations users can generate advisory GPU compute price quotes for H100, A100, L40S, and A10G offerings. The skill supports single-scenario pricing, JSON output, base price lookup, and multi-scenario comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated quotes may be misleading if users rely on them without validating positive counts, durations, and business terms.

Mitigation: Validate inputs and review generated quotes before using them in customer-facing, billing, or contractual workflows.

## Reference(s):

- [Pans Pricing Engine on ClawHub](https://clawhub.ai/dashiming/skills/pans-pricing-engine)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text quote summaries, JSON pricing data, and command-line usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory pricing calculations based on fixed base rates and discount rules in the artifact.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
