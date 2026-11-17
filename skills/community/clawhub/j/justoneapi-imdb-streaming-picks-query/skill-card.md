## Description:

Call GET /api/imdb/streaming-picks-query/v1 for IMDb Streaming Picks through JustOneAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call the JustOneAPI IMDb streaming picks endpoint and retrieve curated streaming title data for content discovery and watchlist research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required API token is passed to the helper with --token and added as a query parameter, which evidence.security says can expose it through process metadata or URL logs.

Mitigation: Use protected environment variables, avoid pasting token values into chat or logs, and prefer a provider-supported authorization header or a skill revision that avoids query-string tokens.

Risk: The security verdict is suspicious because of credential exposure risk, even though no malicious behavior was found.

Mitigation: Review before installation when the token has paid quota, broad account access, or sensitive usage implications; use narrowly scoped tokens and rotate them if exposure is suspected.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_streaming_picks_query&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_streaming_picks_query&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-imdb-streaming-picks-query)
- [Operations Reference](generated/operations.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, JSON]

**Output Format:** [Markdown guidance with inline shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs use of the streamingPicksQuery operation, summarizes the endpoint-specific result, returns raw JSON after the summary, and includes backend error payloads with the operation ID when requests fail.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
