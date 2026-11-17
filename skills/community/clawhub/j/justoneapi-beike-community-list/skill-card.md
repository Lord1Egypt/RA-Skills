## Description:

Call GET /api/beike/community/list/v1 for Beike Community List through JustOneAPI with cityId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query JustOneAPI's Beike community-list endpoint for city-scoped residential community data. It supports workflows that compare community names, unique IDs, average listing prices, and historical price trends for a provided cityId.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is required for requests and this version passes it as a command-line argument and query parameter.

Mitigation: Use a narrowly scoped, revocable token and avoid exposing token values in chat, screenshots, shell history, or logs.

Risk: The skill depends on a focused third-party API endpoint and may return backend errors or endpoint-specific payloads.

Mitigation: Review backend error payloads before acting on results and confirm the operation ID and cityId scope in summaries.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/justoneapi/skills/justoneapi-beike-community-list)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike_community_list&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike_community_list&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Markdown summary followed by raw JSON when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JUST_ONE_API_TOKEN and a cityId query parameter; optional condition and limitOffset query parameters are supported.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
