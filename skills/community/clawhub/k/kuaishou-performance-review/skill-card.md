## Description:

Searches public Kuaishou videos, creator posts, and comments, returning structured engagement data for content and audience analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, marketers, and analysts use the skill to search public Kuaishou videos, review creator posts and comments, and assess engagement for research and content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and video or profile links are sent to GUAIKEI. The security assessment reports a benign verdict with medium confidence, partial script inspection, and an undisclosed third-party data-sharing concern.

Mitigation: Use only search terms and public links you are comfortable sharing with GUAIKEI, and account for the partial-inspection caveat when deciding whether to install or use the skill.

## Reference(s):

- [Usage options](references/options.md)
- [Changelog](references/changelog.md)
- [GUAIKEI service website](https://www.guaikei.com)
- [ClawHub skill release](https://clawhub.ai/why20261/skills/kuaishou-performance-review)
- [Publisher profile](https://clawhub.ai/user/why20261)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON results for agent analysis and content performance review]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Kuaishou data. Monthly-token limits are 30 search results, 50 creator posts, and 60 comments; pay-as-you-go requests have a documented hard cap of 10,000.]

## Skill Version(s):

1.1.2 (source: SKILL.md frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
