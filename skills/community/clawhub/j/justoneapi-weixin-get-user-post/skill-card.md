## Description: <br>
Call GET /api/weixin/get-user-post/v1 for WeChat Official Accounts User Published Posts through JustOneAPI with wxid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query JustOneAPI for published posts from a WeChat Official Account by wxid, then summarize titles, publish times, and summaries for account monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper handles a JustOneAPI token in command-line arguments and request URLs, which can expose the token through shell history, process listings, logs, proxies, or monitoring tools. <br>
Mitigation: Use only with an acceptable JustOneAPI token, avoid pasting token values into chat or logs, prefer secret-store or environment-based token handling, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_user_post&utm_content=project_link) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_user_post&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-weixin-get-user-post) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, JSON, guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON when the endpoint returns data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; non-token input is wxid.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
