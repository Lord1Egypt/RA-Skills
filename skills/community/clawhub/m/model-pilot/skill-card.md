## Description:

Model Pilot helps agents match task complexity to an appropriate model tier, check whether a cheaper model can preserve quality, and estimate costs with live pricing lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tommot2](https://clawhub.ai/user/tommot2)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to decide whether a task needs a higher-capability model, whether a lower-cost model is suitable, and how to estimate model costs before expensive work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model-switch recommendations may trade away quality or select a provider the user does not want.

Mitigation: Review suggested switches before acting, especially when quality, latency, provider choice, or compliance requirements matter.

Risk: Pricing estimates can become outdated or differ from provider billing behavior.

Mitigation: Fetch current provider pricing for cost-sensitive comparisons and treat estimates as advisory.

## Reference(s):

- [Model Database - Pricing, Benchmarks & Capability Tiers](references/model-database.md)
- [Model Pilot on ClawHub](https://clawhub.ai/tommot2/skills/model-pilot)
- [Z.ai Pricing](https://z.ai/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown text with short recommendations, pricing estimates, and inline command examples when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are advisory and depend on live pricing checks when cost accuracy matters.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill title; artifact _meta.json reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
