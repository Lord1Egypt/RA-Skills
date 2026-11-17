## Description:

Call GET /api/weibo/tv-component/v1 for Weibo TV Video Details through JustOneAPI with oid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI's Weibo TV video details endpoint for a supplied Weibo object ID. It supports video research, archiving, and performance analysis by returning media URLs, author details, and engagement counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a JustOneAPI token to api.justoneapi.com and may expose the credential through command lines or URL query strings.

Mitigation: Use a scoped, revocable, low-quota token; avoid environments that log full command lines or URLs; rotate the token if it may have appeared in logs.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_tv_component&utm_content=project_link)
- [Weibo TV Video Details operations](generated/operations.md)
- [OpenAPI operation metadata](generated/operations.json)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; required endpoint input is oid.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
