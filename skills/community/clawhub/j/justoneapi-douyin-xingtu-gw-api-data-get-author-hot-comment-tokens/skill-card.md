## Description: <br>
Call GET /api/douyin-xingtu/gw/api/data/get_author_hot_comment_tokens/v1 for Douyin Creator Marketplace (Xingtu) KOL Comment Keyword Analysis through JustOneAPI with oAuthorId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call JustOneAPI's Douyin Creator Marketplace endpoint for a creator author ID and summarize comment keyword analysis results for audience language and comment-topic research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token is sent to api.justoneapi.com as a URL query parameter, which can be exposed through copied URLs, logs, or diagnostics. <br>
Mitigation: Use a scoped or short-lived JUST_ONE_API_TOKEN when available, avoid logging full request URLs, and rotate the token if exposure is suspected. <br>
Risk: The skill sends requests to a third-party JustOneAPI endpoint. <br>
Mitigation: Install and run it only if you trust justoneapi and the endpoint fits your data handling requirements. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_get_author_hot_comment_tokens&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_get_author_hot_comment_tokens&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-data-get-author-hot-comment-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON from the endpoint when available, with inline shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and oAuthorId; backend errors should include the operation ID and returned payload.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
