## Description:

Retrieves public Kuaishou videos, creator posts, and comments and returns structured engagement data for content research and comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketers, and analysts use this skill to research Kuaishou topics, compare public creator posts, screen creators, and review video comments. It returns structured engagement data for follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanner confidence is medium because inspection was partial, and queries send search terms or links to a third-party service.

Mitigation: Review the service's privacy practices and only submit public-data queries you are comfortable sharing; inspect the scripts before installation.

## Reference(s):

- [Command options](references/options.md)
- [Release changelog](references/changelog.md)
- [Kuaishou data service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON envelopes containing search results, creator data, or comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Engagement fields vary by command; empty results and errors use the documented response envelope.]

## Skill Version(s):

1.1.2 (source: server-resolved release metadata, SKILL.md frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
