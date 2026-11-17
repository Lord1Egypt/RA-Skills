## Description:

Checks whether claims in an Amazon listing match customer review experiences and identifies gaps in the available evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and commerce operators use this skill to compare product page promises with review evidence, identify evidence gaps, and prepare grounded operational findings. It does not provide legal compliance conclusions or publish listing changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quote-only checks may trigger paid analysis, and recurring monitoring may exceed the stated listing-checking scope.

Mitigation: Prefer a corrected release. If proceeding, set ARI to ask every time, use manual collection for one-time work, and review recurring schedules and competitor monitoring.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/funewa/skills/listing-promise)
- [ARI operations](https://ari.funewa.com/zh/operations)
- [ARI monitoring center](https://ari.funewa.com/zh/monitor)
- [Operation workflow](references/operation-workflow.md)
- [ARI API reference](references/reference.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Concise Markdown findings and reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-based findings with data-scope limitations; paid workflows may require user confirmation.]

## Skill Version(s):

1.5.3 (source: changelog; release evidence confirms)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
