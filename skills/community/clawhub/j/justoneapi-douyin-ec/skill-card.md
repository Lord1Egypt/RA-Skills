## Description: <br>
Analyze Douyin E-commerce workflows with JustOneAPI, including item Details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to fetch Douyin E-commerce item details through JustOneAPI when they have an itemId and need an API-backed answer with price, title, stock, and related item fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token for authenticated Douyin item-detail requests. <br>
Mitigation: Install only when the publisher is trusted, keep JUST_ONE_API_TOKEN private, and avoid sharing chat messages, screenshots, or logs that include the token. <br>
Risk: The token is sent in the request URL, which may expose it through verbose proxy, HTTP, or error logging. <br>
Mitigation: Avoid verbose request logging, do not share error logs containing full URLs, and rotate the token if request URLs may have been exposed. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_ec&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_ec&utm_content=project_link) <br>
- [Generated Douyin E-commerce operations](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and API JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and an itemId; backend errors include the backend payload and operation ID.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
