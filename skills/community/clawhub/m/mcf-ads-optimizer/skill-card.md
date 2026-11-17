## Description:

AI-powered ad campaign management with performance audits, optimization analysis, A/B testing, and anomaly detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cameron48](https://clawhub.ai/user/cameron48)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents managing paid media use this skill to create or update campaign configuration, run audits, get optimization recommendations, manage A/B tests, and monitor spending anomalies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live campaign settings and paid-media spend.

Mitigation: Require strict account scope, budget limits, audit logging, and human approval before mutating campaign actions.

Risk: Optimization, A/B test, or anomaly recommendations could affect client budgets or campaign performance if applied without review.

Mitigation: Use a review or dry-run step before execution and maintain a rollback process for campaigns and tests.

## Reference(s):

- [Ads Optimizer on ClawHub](https://clawhub.ai/cameron48/skills/mcf-ads-optimizer)
- [Ads Optimizer API Gateway](https://gateway.mcfagentic.com)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [JSON responses with campaign records, audit findings, optimization recommendations, A/B test status, and anomaly reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Endpoint responses may include projected savings, projected performance impact, severity labels, and recommended actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
