## Description:

Call GET /api/douyin-xingtu/get-video-detail/v1 for Douyin Creator Marketplace (Xingtu) Video Details through JustOneAPI with detailId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external integrators use this skill to call JustOneAPI's Douyin Creator Marketplace (Xingtu) video detail endpoint for a specific detailId and summarize the returned performance-oriented video data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command-line process metadata or URL logs because authentication is passed into a query-token API flow.

Mitigation: Review before installing when the token has quota, billing, or data access; rotate and tightly scope the token if this API flow is required.

Risk: The endpoint sends requests to an external JustOneAPI service and depends on user-provided detailId values.

Mitigation: Confirm required parameters before execution, keep user-provided IDs unchanged, and review backend errors before sharing results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-video-detail)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_video_detail&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_video_detail&utm_content=project_link)
- [Generated operation reference](generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; output guidance asks agents to summarize the endpoint-specific result before returning raw JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
