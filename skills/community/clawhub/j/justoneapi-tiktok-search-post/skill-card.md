## Description:

Call GET /api/tiktok/search-post/v1 for TikTok Post Search through JustOneAPI with keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to search TikTok posts by keyword through JustOneAPI for trend monitoring, content discovery, market analysis, and sentiment tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is passed through command-line arguments and query URLs, where local diagnostics, shell history, process listings, or service logs may expose it.

Mitigation: Use a narrowly scoped token when available, avoid sharing command output that includes request details, and rotate the token if exposure is suspected.

Risk: Paid quota or broad API permissions could be consumed unexpectedly if the token is overprivileged.

Mitigation: Prefer a token with limited scope or quota for this skill and review usage before installing or running it.

Risk: Search keywords and filters may be recorded by the external API provider or local logs.

Mitigation: Avoid sensitive keywords and review the provider's data-handling expectations before using the skill for confidential work.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_search_post&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_search_post&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-tiktok-search-post)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Short Markdown summary followed by raw JSON from the JustOneAPI endpoint]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and the keyword query parameter; optional filters include offset, publishTime, region, and sortType.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
