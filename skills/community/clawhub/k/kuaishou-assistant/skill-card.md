## Description:

Search public Kuaishou videos by keyword, retrieve creators’ public posts and metrics, and analyze video comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and analysts can use the skill to research public Kuaishou videos, creator activity, and comments for topic research, competitor review, and audience analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send keywords or Kuaishou links to the third-party GuaiKei service.

Mitigation: Review the query before running the skill and avoid sending confidential or sensitive information.

## Reference(s):

- [GuaiKei service and token access](https://www.guaikei.com)
- [ClawHub skill release](https://clawhub.ai/why20261/skills/kuaishou-assistant)
- [Command options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON data, Analysis guidance]

**Output Format:** [Structured JSON containing video search results, creator posts or metrics, or video comments.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public data only. Requires a GUAIKEI_API_TOKEN and sends query keywords or links to GuaiKei. Per-request limits depend on the token plan: up to 10,000 for pay-as-you-go; monthly limits are 30 search results, 50 posts, and 60 comments.]

## Skill Version(s):

1.1.1 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
