## Description:

Turns one or more patent texts into sourced, plain-language Markdown for WeChat articles, Xiaohongshu posts, and video scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent teams, company communicators, and content creators use it to turn patent text into accessible public-facing explainers, with technical claims tied back to their patent sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential creation and local cache handling may expose API credentials or cached data.

Mitigation: Review before installation, secure credential creation, and contain cache paths with appropriate access controls.

Risk: Confidential invention details may be included in patent lookups.

Mitigation: Prefer public patent identifiers over confidential invention details.

Risk: Retrying a timed-out paid request may lead to unexpected charges.

Mitigation: Set a spending limit and check billing before retrying a timed-out request.

Risk: Authenticated requests or redirects may reach unintended destinations.

Mitigation: Restrict authenticated destinations and redirects.

## Reference(s):

- [PatentMax API Reference](references/api-reference.md)
- [Patent Query Syntax](references/query-syntax.md)
- [PatentMax API Platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Chinese Markdown tailored to WeChat articles, Xiaohongshu posts, or short video scripts, with patent-source citations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Technical statements are grounded in patent text; unsupported claims and data are excluded.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
