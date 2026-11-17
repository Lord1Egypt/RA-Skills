## Description:

A read-only skill for searching public Kuaishou videos, creator posts and follower data, and video comments, with results returned as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[um-why](https://clawhub.ai/user/um-why)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, and analysts can use the skill to research Kuaishou topics, review public creator activity, and inspect video comments for competitor or audience insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and video links are sent to a third-party service.

Mitigation: Avoid confidential queries and sensitive links; use only information appropriate to share with that service.

Risk: The security evidence says some code was only partially analyzed and notes scope and privacy-transparency questions.

Mitigation: Review the skill's scope and data-handling information before installation.

## Reference(s):

- [Usage options](references/options.md)
- [Release notes](references/changelog.md)
- [Service and token setup](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/um-why/skills/kuaishou-data-miner)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON data for video searches, creator posts and profile metrics, or video comments.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can be empty or report an error status; a service access token is required.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
