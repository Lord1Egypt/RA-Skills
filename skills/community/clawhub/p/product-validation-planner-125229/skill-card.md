## Description:

Helps creators and communicators turn an Ask HN product-help request into a practical workflow, artifact, checklist, analysis, or implementation support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and communicators use this skill to clarify product-validation requests, generate concrete deliverables, and check outputs against stated success criteria. It is useful when a user needs a practical workflow, checklist, analysis, code change, or decision support for a product idea or request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad product-related wording because implicit invocation is enabled and trigger terms are generic.

Mitigation: Review activation behavior before deployment and narrow trigger wording when precise routing is required.

Risk: Generated planning guidance may not fully match the user's product context if important constraints are missing.

Mitigation: Ask for missing information only when it materially changes the output, then validate the result against the stated success criteria.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Ask HN: I Need Help for a Product](https://news.ycombinator.com/item?id=48505805)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/product-validation-planner-125229)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, checklists, workflows, verification notes, and next-step guidance.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
