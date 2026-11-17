## Description:

Call GET /api/twitter/get-user-posts/v1 for Twitter User Published Posts through JustOneAPI with restId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve a Twitter user's published posts through JustOneAPI for account monitoring and content analysis. The required lookup input is the user's numeric restId, with cursor support for pagination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token may be exposed through command arguments or URL query strings when the helper calls JustOneAPI.

Mitigation: Use only where sending the token and queried Twitter user IDs to JustOneAPI is acceptable; avoid logging commands or URLs, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_twitter_get_user_posts&utm_content=project_link)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_twitter_get_user_posts&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-twitter-get-user-posts)
- [Generated Operations Reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with optional raw JSON response payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a Twitter restId; supports an optional pagination cursor.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
