## Description:

Call GET /api/tiktok/search-user/v1 for TikTok User Search through JustOneAPI with keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to search TikTok users by keyword through JustOneAPI and retrieve profile identifiers, nicknames, unique handles, and related search results for influencer discovery, audience research, or competitor research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through URLs, process arguments, or logs.

Mitigation: Use a scoped or short-lived token where available, avoid logging full URLs or command lines, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_search_user&utm_content=project_link)
- [TikTok User Search operations](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, JSON]

**Output Format:** [Markdown summary followed by raw JSON from the API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires operationId searchUserV1, a keyword parameter, and a JustOneAPI token supplied through JUST_ONE_API_TOKEN.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
