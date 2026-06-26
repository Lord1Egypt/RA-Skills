## Description: <br>
Call GET /api/tiktok/get-post-comment/v1 for TikTok Post Comments through JustOneAPI with awemeId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to fetch TikTok post comments for a known awemeId through JustOneAPI. It supports engagement review and sentiment-oriented analysis by returning comment IDs, user information, and comment text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A JustOneAPI token could be exposed through chat, screenshots, shell history, or logged request URLs. <br>
Mitigation: Keep JUST_ONE_API_TOKEN in an environment variable or secret manager, avoid logging full request URLs, and rotate the token if exposure is suspected. <br>
Risk: TikTok post IDs and returned comment or user data may be sensitive or governed by platform and privacy rules. <br>
Mitigation: Share and retain returned comment data only as needed for the user task and handle it according to applicable privacy and platform requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-tiktok-get-post-comment) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_post_comment&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_post_comment&utm_content=project_link) <br>
- [Generated operation reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with optional raw JSON response and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the getPostCommentV1 operation with required awemeId and optional cursor parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
