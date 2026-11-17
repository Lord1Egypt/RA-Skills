## Description:

Retrieve public Kuaishou videos, creator posts, engagement metrics, and comments for content research and performance review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, social media operators, marketers, and analysts can search public Kuaishou videos, review creator posts and comments, and use engagement metrics to inform content and competitor research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and video links are sent to a third-party provider, whose live behavior and data retention have not been verified.

Mitigation: Use a GUAIKEI-specific token and avoid confidential search terms.

Risk: Requests may incur provider plan charges or exceed plan-specific result limits.

Mitigation: Check the applicable plan limits before requesting larger result sets.

Risk: Optional logging retains local copies of results.

Mitigation: Enable logging only when retained local copies are needed.

## Reference(s):

- [Usage options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON response envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public video search results, creator posts or profile metrics, and comments; result limits depend on the provider plan.]

## Skill Version(s):

1.1.1 (source: release evidence, frontmatter, changelog, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
