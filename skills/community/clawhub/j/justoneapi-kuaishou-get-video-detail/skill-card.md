## Description:

Call GET /api/kuaishou/get-video-detail/v2 for Kuaishou Video Details through JustOneAPI with videoId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Kuaishou video detail data from JustOneAPI by videoId, including video URL, caption, and author information for content analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through local process metadata or shared command logs.

Mitigation: Use a narrowly scoped, revocable token; avoid sharing logs or process listings from runs; and rotate the token if exposure is possible.

Risk: The token is sent to JustOneAPI as a query parameter, which can increase exposure through URL logging.

Mitigation: Monitor quota or billing, restrict token permissions where supported, and run the skill only in trusted environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-kuaishou-get-video-detail)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_video_detail&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_video_detail&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Short Markdown summary followed by raw JSON from the API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, a JustOneAPI token, and a Kuaishou videoId.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
