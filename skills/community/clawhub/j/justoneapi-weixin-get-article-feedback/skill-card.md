## Description: <br>
Call GET /api/weixin/get-article-feedback/v1 for WeChat Official Accounts Article Engagement Metrics through JustOneAPI with articleUrl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call JustOneAPI's WeChat Official Accounts article engagement endpoint for like, share, and comment metrics on a supplied article URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token and the security summary says token handling can expose credentials unnecessarily. <br>
Mitigation: Install only if you trust JustOneAPI, avoid sharing command lines or logs that include tokens, and rotate the token if exposure is suspected. <br>
Risk: The token is passed on the command line and sent as a URL query parameter. <br>
Mitigation: Prefer a revised version that reads credentials from a protected secret source and uses header-based authentication if the upstream API supports it. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_article_feedback&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_article_feedback&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-weixin-get-article-feedback) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; the endpoint requires articleUrl.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
