## Description: <br>
Call GET /api/tiktok/get-post-sub-comment/v1 for TikTok Comment Replies through JustOneAPI with awemeId and commentId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve TikTok comment replies for a specific post and parent comment through JustOneAPI. It supports review of threaded discussions, reply text, user information, and active participants in a comment section. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API token handling can expose the token in URLs, command history, process listings, or logs. <br>
Mitigation: Run the skill in a private environment, pass tokens through the documented environment variable, avoid pasting tokens into chat or logs, and rotate the token if exposure is possible. <br>
Risk: The skill sends TikTok post and comment identifiers, along with the API token, to the JustOneAPI service. <br>
Mitigation: Use it only when the API provider is trusted with the token and request data, and review endpoint inputs before execution. <br>


## Reference(s): <br>
- [JustOneAPI API homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_post_sub_comment&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-tiktok-get-post-sub-comment) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Markdown guidance, Shell commands] <br>
**Output Format:** [Markdown summary followed by raw JSON from the JustOneAPI endpoint.] <br>
**Output Parameters:** [1D; requires awemeId and commentId, accepts optional cursor, and uses JUST_ONE_API_TOKEN for authentication.] <br>
**Other Properties Related to Output:** [Requires Node.js and a JustOneAPI token. The token is passed to the helper and sent as a query parameter to the API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
