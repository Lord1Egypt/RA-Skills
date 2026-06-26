## Description: <br>
Call GET /api/zhihu/search/v1 for Zhihu Keyword Search through JustOneAPI with keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to query JustOneAPI's Zhihu keyword search endpoint for topic discovery and content research using a keyword, with an optional offset for paging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is passed as a command-line argument and sent in the request URL, which can expose it through local process inspection, shell history, logs, monitoring, or error reports. <br>
Mitigation: Install only where that exposure is acceptable, avoid logging command lines or request URLs, and rotate the token if exposure is suspected. <br>
Risk: Credential handling depends on a token-bearing query parameter for the documented endpoint. <br>
Mitigation: Prefer a revised version that reads the token directly from the environment and uses an authorization header if the service supports it. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_search&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_search&utm_content=project_link) <br>
- [ClawHub release page](https://clawhub.ai/justoneapi/justoneapi-zhihu-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with a Node.js command example and JSON API response output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a keyword; optional offset defaults to 0.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
