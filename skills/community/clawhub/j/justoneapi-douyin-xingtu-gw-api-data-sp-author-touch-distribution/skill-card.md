## Description:

Call GET /api/douyin-xingtu/gw/api/data_sp/author_touch_distribution/v1 for Douyin Creator Marketplace (Xingtu) Audience Touchpoint Distribution through JustOneAPI with oAuthorId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and marketing analysts use this skill to query JustOneAPI for Douyin Creator Marketplace (Xingtu) audience touchpoint distribution data for creator evaluation, campaign planning, and marketplace research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command-line process listings or full request URL logs.

Mitigation: Use a narrowly scoped, revocable token, avoid logging command lines or full request URLs, and rotate the token if exposure is suspected.

Risk: The skill sends the token and query parameters to the JustOneAPI Douyin/Xingtu endpoint.

Mitigation: Install and run the skill only when sharing the token and requested creator identifier with JustOneAPI is acceptable for the intended workflow.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_touch_distribution&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-gw-api-data-sp-author-touch-distribution)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown summary with optional raw JSON response from the API helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and an oAuthorId query parameter; platform defaults to SHORT_VIDEO when omitted.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
