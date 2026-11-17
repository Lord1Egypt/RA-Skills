## Description:

Verify that a blog post, tweet, thread, or LinkedIn post aligns to at least one of the 6 Redditech Labs content pillars before drafting or publishing content for @redditech or Redditech Labs, returning a primary pillar, optional secondary pillar, alignment score, and pass/flag/reject verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Content and growth agents or reviewers use this skill to check Redditech Labs draft posts against six content pillars, brand voice rules, and escalation criteria before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The rubric encodes Redditech Labs-specific content pillars, AEST timing, and Nissan escalation assumptions that may not fit another publishing team.

Mitigation: Review and adapt the pillars, timezone, escalation owner, and publishing process before deployment.

Risk: A pass, flag, or reject verdict could approve or block content based on brand-fit criteria without replacing factual, legal, or final editorial review.

Mitigation: Keep human review for final publishing decisions, especially rejected content, DeFi/Web3 topics, and claims that require evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/pillar-alignment-check)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown assessment block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes primary pillar, optional secondary pillar, alignment score, pass/flag/reject verdict, reason, and action when escalation or redrafting is required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
