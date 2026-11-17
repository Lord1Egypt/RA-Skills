## Description:

Call GET /api/imdb/title-more-like-this-query/v1 for IMDb Recommendations through JustOneAPI with an IMDb title ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up IMDb recommendations for a title ID through JustOneAPI and summarize related-title suggestion data for content discovery or recommendation analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can leak through command metadata, shell history, request URLs, proxy logs, or server logs.

Mitigation: Use a limited, easily rotated token; avoid command and request tracing; rotate the token if exposure is suspected.

Risk: The skill depends on a live third-party API and may return backend errors or non-JSON responses.

Mitigation: Surface the backend payload and operation ID when failures occur so the caller can retry or troubleshoot without exposing secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-imdb-title-more-like-this-query)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_more_like_this_query&utm_content=project_link)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_more_like_this_query&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and a JUST_ONE_API_TOKEN; the endpoint requires an IMDb title ID and supports an optional languageCountry value.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
