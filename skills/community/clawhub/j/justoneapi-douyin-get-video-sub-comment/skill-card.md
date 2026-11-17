## Description:

Call GET /api/douyin/get-video-sub-comment/v1 for Douyin (TikTok China) Comment Replies through JustOneAPI with commentId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Douyin comment replies by commentId through JustOneAPI for thread analysis and feedback research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JustOneAPI token exposure through command-line arguments and URL query parameters.

Mitigation: Use narrowly scoped, revocable tokens; avoid sharing command logs or process telemetry; rotate the token if it may have appeared in logs.

Risk: Broad permissions, billing impact, or long token lifetime can increase the impact of misuse.

Mitigation: Review token scope and lifetime before installation and prefer a limited token for this endpoint.

## Reference(s):

- [JustOneAPI API homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_video_sub_comment&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_video_sub_comment&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-get-video-sub-comment)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown summary with JSON API response and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; required lookup parameter is commentId.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
