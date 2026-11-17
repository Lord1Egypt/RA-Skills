## Description:

Call GET /api/tiktok/get-post-comment/v1 for TikTok Post Comments through JustOneAPI with awemeId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI's TikTok post comments endpoint for a supplied awemeId, optionally with a pagination cursor. It supports retrieving comment IDs, user information, and text content for audience reaction review and engagement measurement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a JustOneAPI token for TikTok comment lookups, and token exposure in chat, shell history, process logs, or URL logs could allow unauthorized API use.

Mitigation: Use a narrowly scoped, revocable token when possible; pass it through JUST_ONE_API_TOKEN; avoid sharing logs that include token-bearing command lines or URLs; rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-tiktok-get-post-comment)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_post_comment&utm_content=project_link)
- [TikTok Post Comments Operations](generated/operations.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON from the API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; required endpoint input is awemeId, with optional cursor pagination.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
