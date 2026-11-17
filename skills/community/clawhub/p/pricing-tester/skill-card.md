## Description:

Design and evaluate A/B tests for different price points, discount levels, and bundle combinations to find the highest-converting offer structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, growth teams, and analysts use this skill to plan, run, and interpret pricing, discount, shipping, and bundle tests with profit per visitor as the primary decision metric.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pricing recommendations may be treated as automatic authority for live business changes.

Mitigation: Review the recommendation against margin data, legal requirements, discount truthfulness, and guardrail metrics before changing production prices.

Risk: Poorly designed tests can produce misleading winners through underpowered samples, peeking, segment leakage, or conversion-rate-only optimization.

Mitigation: Predefine sample size, duration, primary metric, guardrails, and stopping rules, then judge results on profit per visitor with confidence intervals.

## Reference(s):

- [Output Template](references/output-template.md)
- [Experiment Design Guide](references/experiment-design-guide.md)
- [Pricing Test Patterns](references/pricing-test-patterns.md)
- [Pricing Test Quality Checklist](assets/quality-checklist.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Configuration instructions]

**Output Format:** [Markdown guidance with tables, formulas, checklists, and decision templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces business guidance for pricing experiments; users should validate legal compliance, statistical assumptions, and live pricing changes before rollout.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
