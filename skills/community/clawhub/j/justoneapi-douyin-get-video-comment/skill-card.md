## Description:

Call GET /api/douyin/get-video-comment/v1 for Douyin (TikTok China) Video Comments through JustOneAPI with awemeId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call the JustOneAPI Douyin comments endpoint for a specific awemeId and summarize returned comment, author, text, and like data for sentiment analysis or engagement review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command arguments or URL logging.

Mitigation: Use a limited-scope token, avoid running commands in environments that log process arguments, and review logs for token exposure risk.

Risk: Returned Douyin comments are user-generated content and may carry privacy or platform-terms obligations.

Mitigation: Handle returned comment data according to applicable privacy requirements and Douyin or JustOneAPI terms before sharing or storing it.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_video_comment&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_video_comment&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-get-video-comment)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token, awemeId, and optional page query parameter.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
