## Description:

Call GET /api/weibo/search-profile/v1 for Weibo Search User Published Posts through JustOneAPI with q and uid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query JustOneAPI for Weibo user published posts by UID and search keyword. It supports author research and historical content discovery by returning matched results, metadata, and ranking signals from the documented endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is passed through command arguments and sent as a URL query parameter, which may expose it in process listings or URL logs.

Mitigation: Use a narrowly scoped token if available, avoid shared machines and verbose command or process logging, monitor usage, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_search_profile&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_search_profile&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-weibo-search-profile)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses operation ID searchProfileV1 and endpoint path /api/weibo/search-profile/v1; requires uid, q, and a JustOneAPI token.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
