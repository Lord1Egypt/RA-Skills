## Description: <br>
Call GET /api/reddit/get-post-comments/v1 for Reddit Post Comments through JustOneAPI with postId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Reddit post comments through JustOneAPI for discussion analysis and moderation research, using a postId and optional pagination cursor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a JustOneAPI token and Reddit post IDs to JustOneAPI. <br>
Mitigation: Use a scoped, rotatable token and revoke it if it may have been exposed. <br>
Risk: Full request URLs, logs, or command output may expose sensitive token or lookup details. <br>
Mitigation: Avoid sharing logs or screenshots that include request URLs, tokens, post IDs, or backend error payloads. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_reddit_get_post_comments&utm_content=project_link) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_reddit_get_post_comments&utm_content=project_link) <br>
- [Generated operation reference](artifact/generated/operations.md) <br>
- [ClawHub release page](https://clawhub.ai/justoneapi/justoneapi-reddit-get-post-comments) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, JSON] <br>
**Output Format:** [Markdown summary with operation details and optional raw JSON response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN; uses postId and optional cursor query parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
