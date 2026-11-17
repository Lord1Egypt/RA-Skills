## Description:

Call GET /api/bilibili/get-video-danmu/v2 for Bilibili Video Danmaku through JustOneAPI with aid and cid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Bilibili video danmaku by AID and CID through JustOneAPI, then summarize timeline positions and comment text for audience reaction analysis or subtitle-style review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed because the skill sends it in the request URL and accepts it through process arguments.

Mitigation: Install only if that handling is acceptable, avoid sharing logs or command histories that may contain the token, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_danmu&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_danmu&utm_content=project_link)
- [Bilibili Video Danmaku operations](generated/operations.md)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-bilibili-get-video-danmu)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Endpoint-specific summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and JUST_ONE_API_TOKEN; required endpoint inputs are aid and cid, with optional page.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
