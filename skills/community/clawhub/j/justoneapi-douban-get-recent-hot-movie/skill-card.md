## Description:

Call GET /api/douban/get-recent-hot-movie/v1 for Douban Movie Recent Hot Movie through JustOneAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to call JustOneAPI's Douban Movie recent hot movie endpoint, retrieve ratings, posters, and subject metadata, and summarize movie discovery or trend monitoring results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token can be exposed through command arguments and request URLs.

Mitigation: Use a narrowly scoped, revocable JustOneAPI token, avoid running the helper on shared systems where process arguments may be visible, and rotate the token if command logs or URL logs may capture it.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_recent_hot_movie&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_recent_hot_movie&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douban-get-recent-hot-movie)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown summary with raw JSON API response when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses operation getRecentHotMovieV1 with required JUST_ONE_API_TOKEN authentication and optional page pagination.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
