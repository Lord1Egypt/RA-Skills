## Description:

Pull the people who liked or commented on any LinkedIn post and segment them by ICP fit, producing an engager roster, tier breakdown, and outbound action lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, marketing, and founder-led growth users use this skill to analyze LinkedIn post engagers, group them by ICP fit, and produce follow-up action lists for relationship building or outreach review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LinkedIn engagement analysis can create privacy or permission concerns when run on audiences the user does not own or have permission to analyze.

Mitigation: Keep runs limited to posts the user owns or is explicitly permitted to analyze.

Risk: Outbound recommendations may be inappropriate, inaccurate, or too aggressive if used without review.

Mitigation: Review all outreach suggestions before use and delay same-day direct messages as the skill guidance recommends.

Risk: Apify usage can incur costs as max engager counts increase.

Mitigation: Set conservative max engager limits and monitor Apify costs before scaling repeated runs.

## Reference(s):

- [Engager analytics output spec](references/output-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables and action lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an engager roster, ICP tier breakdown, and prioritized follow-up lists with one-line opener seeds.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
