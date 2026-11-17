## Description:

Call GET /api/instagram/search-reels/v1 for Instagram Reels Search through JustOneAPI with keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to search Instagram Reels by keyword or hashtag through JustOneAPI. It supports trend tracking and discovery of high-engagement reels by returning endpoint-specific result data such as post IDs, captions, and author profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command arguments or URL query logs.

Mitigation: Use a short-lived, low-scope token where possible, avoid pasting token values into chat or logs, and rotate the token if it may have been exposed.

Risk: The skill requires access to an external JustOneAPI endpoint and may return backend error payloads.

Mitigation: Review backend error payloads before sharing them and avoid including credentials, sensitive search terms, or private operational context in support requests.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_search_reels&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_search_reels&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-instagram-search-reels)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with JSON response payloads and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses operation searchReelsV1 on /api/instagram/search-reels/v1; accepts keyword and optional paginationToken.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
