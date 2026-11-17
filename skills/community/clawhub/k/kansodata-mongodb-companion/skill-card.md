## Description:

Companion skill de MongoDB para consultas y análisis read-only, con degradación y rechazo fail-closed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kansodata](https://clawhub.ai/user/kansodata)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, constrain, and explain read-only MongoDB inspections, document queries, aggregations, and result interpretation through the configured mongodb plugin. It is intended to fail closed when requests are ambiguous, unsupported, or outside the read-only boundary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a configured mongodb plugin and cannot provide observed database results when that plugin is unavailable.

Mitigation: Install it only where the mongodb plugin is configured for the intended read-only databases, and require the agent to state insufficient context rather than simulate access.

Risk: Users may ask for writes, administrative changes, migrations, repairs, or operational validation that are outside the skill's read-only scope.

Mitigation: Keep the fail-closed boundary active: reject mutation or administration requests and offer only permitted read-only next steps.

Risk: The artifact appears to force Spanish structured responses, which may not match every deployment's user expectations.

Mitigation: Review localization requirements before deployment and override or revise response-language behavior when the target users need another language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kansodata/skills/kansodata-mongodb-companion)
- [ClawHub publisher profile](https://clawhub.ai/user/kansodata)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses follow a fixed evidence-first pattern with result, observed evidence, limits, confidence level, maturity state, and a permitted read-only next step.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
