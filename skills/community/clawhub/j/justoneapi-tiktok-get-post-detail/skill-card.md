## Description:

Call GET /api/tiktok/get-post-detail/v1 for TikTok Post Details through JustOneAPI with postId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to retrieve TikTok post detail data through JustOneAPI by providing a postId. It supports content performance analysis, metadata extraction, and influencer evaluation using the documented getTiktokPostDetailV1 endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required JustOneAPI token may be exposed through command arguments or request URLs.

Mitigation: Use a narrowly scoped or short-lived token, avoid environments that log process arguments or full URLs, and rotate the token if exposure is suspected.

Risk: Backend error payloads may contain details from the API request or response.

Mitigation: Review error output before sharing logs and avoid pasting token values into chat messages, screenshots, or telemetry.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-tiktok-get-post-detail)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_post_detail&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_post_detail&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown summary with raw JSON response data and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; required endpoint input is postId.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
