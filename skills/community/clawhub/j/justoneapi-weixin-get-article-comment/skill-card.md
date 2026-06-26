## Description: <br>
Call GET /api/weixin/get-article-comment/v1 for WeChat Official Accounts Article Comments through JustOneAPI with articleUrl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve WeChat Official Accounts article comments from JustOneAPI by article URL for feedback analysis. It is intended for workflows that need commenter details, comment text, and timestamps from the documented endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required API token may be exposed through command lines, request URLs, or logs. <br>
Mitigation: Use a low-scope token if available, avoid logging command lines or request URLs, and rotate the token if exposure is suspected. <br>
Risk: Returned commenter details, comment text, and timestamps may contain personal information. <br>
Mitigation: Treat returned data as potentially personal information and handle it according to the user's privacy, retention, and access-control requirements. <br>


## Reference(s): <br>
- [JustOneAPI API homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_article_comment&utm_content=project_link) <br>
- [ClawHub skill release](https://clawhub.ai/justoneapi/justoneapi-weixin-get-article-comment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown summary with optional raw JSON response payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and articleUrl; results may include commenter details, comment text, and timestamps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
