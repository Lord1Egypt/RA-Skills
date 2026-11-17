## Description:

Queries public X/Twitter posts, replies, user profiles, searches, trends, and interactions through the MaxHub API for social listening and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Public relations teams, cross-border marketers, and researchers use the skill to examine public X/Twitter posts, users, trends, and interactions for media monitoring, account analysis, and content research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, account identifiers, URLs, and the API credential may be sent to the third-party MaxHub service.

Mitigation: Use the service only for authorized requests, minimize the identifiers and search terms supplied, and keep MAXHUB_API_KEY out of logs and prompts.

Risk: The security review reports local compliance-record writes, an additional balance-query capability, an unpinned installer, and incomplete reference coverage.

Mitigation: Review the installed release and its requested behavior before use; limit local and network access to what the task requires, and verify the release source.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-twitter)
- [ClawHub release page](https://clawhub.ai/xiewxx/skills/maxhub-twitter-pro)
- [Publisher profile](https://clawhub.ai/user/xiewxx)
- [MaxHub API service](https://www.aconfig.cn)
- [Endpoint whitelist](references/endpoints_whitelist.yaml)
- [Recipe index](references/recipes/_index.md)
- [Parameter mappings](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, JSON, Markdown, Guidance]

**Output Format:** [Markdown summaries and structured findings derived from API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented social data queries; results may include user-generated content and personal data.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
