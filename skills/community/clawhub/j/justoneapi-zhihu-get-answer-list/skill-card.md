## Description: <br>
Call GET /api/zhihu/get-answer-list/v1 for Zhihu Answer List through JustOneAPI with questionId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to call JustOneAPI's Zhihu answer-list endpoint for a question ID, then summarize answer content, author profiles, and interaction metrics for question analysis and answer research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token may be exposed through command arguments or request URLs. <br>
Mitigation: Use only in a trusted local environment, avoid logging full commands or request URLs, and rotate the token if it may have appeared in logs. <br>
Risk: The helper sends the token as a query parameter for the JustOneAPI request. <br>
Mitigation: Prefer a revised version that reads the token from a secure source and sends it in an Authorization or API-key header if the provider supports it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-zhihu-get-answer-list) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_get_answer_list&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_get_answer_list&utm_content=project_link) <br>
- [Generated operations reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with optional raw JSON response and inline shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a questionId; optional cursor, offset, order, and sessionId query parameters are supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
