## Description:

Helps agents recommend SaaS and software marketing ideas, strategies, and tactics tailored to a user's product, audience, stage, resources, and growth goal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coreyhaines31](https://clawhub.ai/user/coreyhaines31)

### License/Terms of Use:

MIT-0

## Use Case:

External users, founders, and marketing teams use this skill to brainstorm and prioritize SaaS or software growth tactics. The skill helps match marketing ideas to stage, budget, team size, timeline, and growth goal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read local product-marketing context files to tailor recommendations, which can surface sensitive product or strategy details in responses.

Mitigation: Review product-marketing context files before invoking the skill and remove confidential information that should not influence generated recommendations.

Risk: Marketing recommendations can be mismatched when product stage, audience, budget, or prior experiments are unclear.

Mitigation: Confirm the user's stage, growth goal, budget, team size, and previous marketing results before acting on the suggested tactics.

## Reference(s):

- [The 139 Marketing Ideas](references/ideas-by-category.md)
- [ClawHub marketing-ideas skill page](https://clawhub.ai/coreyhaines31/skills/marketing-ideas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured recommendations with idea name, fit rationale, starting steps, expected outcome, and resource needs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter metadata.version reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
