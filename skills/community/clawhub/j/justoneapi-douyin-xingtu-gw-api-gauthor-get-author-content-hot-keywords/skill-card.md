## Description: <br>
Call GET /api/douyin-xingtu/gw/api/gauthor/get_author_content_hot_keywords/v1 for Douyin Creator Marketplace (Xingtu) KOL Content Keyword Analysis through JustOneAPI with oAuthorId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external analysts use this skill to call the JustOneAPI Douyin/Xingtu endpoint for a creator author ID and summarize keyword, trend, and performance signals for content theme analysis and creator positioning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent in the request URL, so it may be exposed through logs, browser history, proxies, or captured command lines. <br>
Mitigation: Use a scoped, revocable token in JUST_ONE_API_TOKEN, avoid logging full request URLs or command lines, and rotate the token if exposure is suspected. <br>
Risk: The skill sends requests to a third-party API service operated by JustOneAPI. <br>
Mitigation: Install and use it only if you trust JustOneAPI and the data handling requirements for this endpoint fit your use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-gauthor-get-author-content-hot-keywords) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_gauthor_get_author_content_hot_keywords&utm_content=project_link) <br>
- [Generated operation reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; calls one documented GET endpoint with oAuthorId.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
