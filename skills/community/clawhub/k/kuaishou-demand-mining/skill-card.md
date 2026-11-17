## Description:

Fetches Kuaishou comments for clustering and sentiment analysis, identifying recurring pain points, feature requests, and unmet needs with supporting source text, and also searches videos and retrieves public creator posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, and analysts use this skill to explore public Kuaishou videos, creator posts, and comments for content research, competitor monitoring, and audience feedback analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Kuaishou links are sent to GUAIKEI when the skill runs.

Mitigation: Use only public data and query details that are appropriate to share with the GUAIKEI service.

Risk: The benign security verdict has medium confidence because inspection covered some components only partially.

Mitigation: Review the skill and consider the security guidance before installation; treat the verdict as limited assurance.

Risk: Returned timestamps use a fixed Beijing time format and may be mistaken for local time.

Mitigation: Check the timestamp convention and convert it to the intended time zone before comparing or reporting results.

## Reference(s):

- [GUAIKEI service and token access](https://www.guaikei.com)
- [Kuaishou Demand Mining ClawHub release](https://clawhub.ai/why20261/skills/kuaishou-demand-mining)
- [Command options](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [Structured JSON data with concise natural-language findings and supporting comment excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieves public video, creator, and comment data; results may be empty or report service and plan limits.]

## Skill Version(s):

1.1.1 (source: artifact/SKILL.md frontmatter, artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
