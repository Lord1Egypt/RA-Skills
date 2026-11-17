## Description:

Analyzes post and account performance, checks whether the data is complete, and turns supported findings into evidence-backed content recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[posteyai](https://clawhub.ai/user/posteyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users managing Postey accounts use this skill to understand post and account performance and choose next content experiments based on the available evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing, delayed, or partial analytics can make comparisons and recommendations misleading.

Mitigation: Check data availability first, compare only posts with usable data, and state limitations such as small samples and timing confounds.

Risk: The skill reads account and post performance data through the connected Postey integration.

Mitigation: Review the Postey integration's permissions before connecting accounts.

## Reference(s):

- [Postey Analytics on ClawHub](https://clawhub.ai/posteyai/skills/postey-analytics)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown with observations, evidence, caveats, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations include supporting evidence and caveats; conclusions are limited by data completeness and sample size.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
