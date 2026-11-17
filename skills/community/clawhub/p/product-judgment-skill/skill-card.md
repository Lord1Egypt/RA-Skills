## Description:

A demand-review skill for product managers and AI agents that evaluates product ideas before PRDs or engineering commitments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longfellow1](https://clawhub.ai/user/longfellow1)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, product teams, and AI agents use it to anchor a demand in a real user and scenario, assess assumptions and evidence, then recommend whether to build, validate, reframe, reduce scope, or stop before a PRD or engineering commitment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated recommendations may be unreliable when user context or supporting evidence is incomplete.

Mitigation: Provide a concrete user, triggering scenario, current workaround, and evidence; review the generated judgment before relying on or committing it.

Risk: The meeting example may involve sensitive participant information.

Mitigation: Obtain participant consent and use approved processing tools or redacted samples.

## Reference(s):

- [Server-resolved source repository](https://github.com/Longfellow1/Product-Judgment-skill)
- [Product Judgment ClawHub release](https://clawhub.ai/longfellow1/skills/product-judgment-skill)
- [Yu-Jun methodology](references/yu-jun-methodology.md)
- [User value equation](references/user-value-equation.md)
- [Fake demand patterns](references/fake-demand-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, JSON]

**Output Format:** [Conversational guidance, Markdown judgment records, and optional JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One demand review per run; the workflow gathers user context and evidence before giving a recommendation.]

## Skill Version(s):

0.1.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
