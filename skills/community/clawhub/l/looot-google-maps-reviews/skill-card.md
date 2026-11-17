## Description:

Read Google Maps reviews. Use when the user says things like "get the reviews for this Google Maps place", "what do customers complain about at this restaurant" or "pull the latest reviews with owner replies". Runs through looot, billed per call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walidboulanouar](https://clawhub.ai/user/walidboulanouar)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve reviews for a Google Maps place and use the skill to understand customer feedback. It summarizes review themes, ratings, and owner replies for a chosen review count.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A review retrieval call incurs a provider charge, which can grow with the requested review count or batch size.

Mitigation: Show the endpoint price and get approval before the first billed run; set a review count and report the total after a batch.

## Reference(s):

- [looot setup instructions](https://looot.ai/skill.md)
- [Google Maps reviews skill page](https://looot.ai/agent-skills/google-maps-reviews)
- [ClawHub release page](https://clawhub.ai/walidboulanouar/skills/looot-google-maps-reviews)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [A review summary with themes, star ratings, at most one short quote, and the number of reviews read.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes retrieved review data and may include owner replies.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
