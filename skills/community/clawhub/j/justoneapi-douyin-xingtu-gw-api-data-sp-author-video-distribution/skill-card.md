## Description:

Call GET /api/douyin-xingtu/gw/api/data_sp/author_video_distribution/v1 for Douyin Creator Marketplace (Xingtu) Video Distribution through JustOneAPI with oAuthorId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call the JustOneAPI Douyin Creator Marketplace (Xingtu) video distribution endpoint for creator evaluation, campaign planning, and marketplace research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is passed through the command line and query string, where it may appear in process listings, shell history, URL logs, or backend logs.

Mitigation: Use a narrowly scoped or short-lived token when available, avoid logging full commands or URLs, keep the token out of chat and screenshots, and rotate it if exposure is suspected.

Risk: Requests send the oAuthorId and authentication token to JustOneAPI.

Mitigation: Install and run the skill only when sharing those values with JustOneAPI is acceptable for the intended workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-data-sp-author-video-distribution)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_video_distribution&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_video_distribution&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Markdown summary with raw JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and oAuthorId; optional platform defaults to SHORT_VIDEO.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
