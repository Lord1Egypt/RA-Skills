## Description:

Retrieves public Kuaishou videos, creator posts, and comments for content and market research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and analysts use this skill to search public Kuaishou videos, review creator posts and comments, and inform content or market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, profile or video URLs, request parameters, and the API token are sent to a third-party service.

Mitigation: Use only approved public-data queries and a dedicated token; confirm that sharing these inputs with guaikei.com is acceptable.

Risk: Fetched results are saved locally in logs.

Mitigation: Review, protect, and delete local logs according to your data-retention policy.

## Reference(s):

- [Skill listing on ClawHub](https://clawhub.ai/why20261/skills/kuaishou-data-research)
- [API provider and support](https://www.guaikei.com)
- [Options and usage](references/options.md)
- [Release notes](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON results with an optional text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes status and request details; fetched results are also saved in local logs.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
