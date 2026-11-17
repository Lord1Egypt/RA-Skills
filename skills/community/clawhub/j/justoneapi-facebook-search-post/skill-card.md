## Description:

Call GET /api/facebook/search-post/v1 for Facebook Post Search through JustOneAPI with keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to search public Facebook posts by keyword through JustOneAPI and summarize matched results, metadata, ranking signals, engagement, and reach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a JustOneAPI token through command-line arguments and request URLs, which may expose the token in local process telemetry or service-side URL logs.

Mitigation: Use short-lived or narrowly scoped tokens, rotate tokens after testing, avoid sensitive search keywords, and review before installing with a real token.

## Reference(s):

- [JustOneAPI API homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_search_post&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_search_post&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown summary with shell command examples and optional raw JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN environment token; required lookup input is keyword, with optional startDate, endDate, and cursor query parameters.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
