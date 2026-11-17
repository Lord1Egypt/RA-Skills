## Description:

India Tax Helper guides resident salaried taxpayers in India through employer declarations, tax filing documents, common interest and investment income, and conservative calculator-backed estimates when FY rules are verified.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aritrocoder](https://clawhub.ai/user/aritrocoder)

### License/Terms of Use:

MIT-0

## Use Case:

External resident salaried taxpayers in India use this skill to understand employer tax declarations, Form 12BB, Form 16, AIS/TIS/26AS, ITR filing, FD/RD taxation, loan-related deductions, capital gains basics, and approximate tax outcomes. The skill is intended to answer conservatively and fail closed when FY-specific rules, rates, dates, or source manifests cannot be verified.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: Tax-rule packaging and calculators may be inconsistent enough that users could over-rely on non-final estimates.

Mitigation: Treat outputs as conceptual guidance, verify rates, deadlines, form applicability, and calculator results manually against official sources before relying on them.

Risk: Missing FY rules, missing source manifests, or known calculation issues can make FY-sensitive tax estimates unreliable.

Mitigation: Fail closed unless the relevant FY rules and sources are verified, and clearly scope any calculator output as approximate when known issues remain.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aritrocoder/skills/india-tax-helper)
- [Skill Overview](references/overview.md)
- [Source Policy](references/source-policy.md)
- [Live Grounding](references/live-grounding.md)
- [Forms Map](references/forms-map.md)
- [Lifecycle Calendar](references/lifecycle-calendar.md)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, guidance, shell commands]

**Output Format:** [Plain text with optional JSON calculator inputs and outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses deterministic JSON-in/JSON-out calculators for estimates and should refuse confident FY-sensitive answers when verified rules are unavailable.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
