## Description: <br>
Analyze Amazon workflows with JustOneAPI, including product Details, product Top Reviews, and best Sellers across 4 operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch API-backed Amazon product details, top reviews, best-seller lists, and category product data through JustOneAPI when the user provides the required identifiers or filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent in request URLs, which can expose credentials through logs, shell history, screenshots, or shared traces. <br>
Mitigation: Use a dedicated revocable token and avoid sharing command traces, full request URLs, logs, or screenshots that may contain the token. <br>
Risk: Backend error payloads may include sensitive request or service details. <br>
Mitigation: Review backend errors before sharing them and redact tokens or sensitive request context. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/justoneapi/justoneapi-amazon) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon&utm_content=project_link) <br>
- [Amazon operations reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with command examples and API-backed response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN for authenticated requests to api.justoneapi.com.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
