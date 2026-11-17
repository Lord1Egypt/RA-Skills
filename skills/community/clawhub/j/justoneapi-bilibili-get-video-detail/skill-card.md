## Description:

Call GET /api/bilibili/get-video-detail/v2 for Bilibili Video Details through JustOneAPI with bvid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to fetch Bilibili video detail metadata by BVID through JustOneAPI for content analysis and performance tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Bilibili video IDs and a JustOneAPI token to api.justoneapi.com.

Mitigation: Use a limited, revocable token when possible and only run the skill when sending those inputs to JustOneAPI is acceptable.

Risk: Token values can be exposed through command lines, request URLs, screenshots, or logs.

Mitigation: Avoid logging full command lines or request URLs, do not paste token values into chat, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_detail&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_detail&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-bilibili-get-video-detail)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, JSON, Guidance]

**Output Format:** [Markdown summary with endpoint details, helper command guidance, and raw JSON response when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; required endpoint input is bvid.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
