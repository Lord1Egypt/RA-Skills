## Description:

Call GET /api/youku/get-video-detail/v1 for YOUKU Video Details through JustOneAPI with videoId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up detailed YOUKU video metadata by videoId through the JustOneAPI endpoint, then summarize the returned fields for dashboards or analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A JustOneAPI token is required and may be exposed through command logs, process listings, or full request URLs.

Mitigation: Use a scoped or short-lived token when available, avoid sharing command logs or full URLs, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku_get_video_detail&utm_content=project_link)
- [YOUKU Video Details operation reference](generated/operations.md)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-youku-get-video-detail)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summary with endpoint details, plus raw JSON for successful API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and videoId; reports operation-specific error details when the endpoint call fails.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
