## Description: <br>
Analyze Taobao and Tmall workflows with JustOneAPI, including product Details, product Reviews, and shop Product List across 10 operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, ecommerce analysts, and agents use this skill to retrieve Taobao and Tmall product details, reviews, shop product lists, and product search results through JustOneAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is included in request URLs and may appear in logs, browser histories, proxies, or error traces. <br>
Mitigation: Use a token scoped to JustOneAPI, keep logs and traces private, redact full request URLs before sharing, and rotate the token if exposure is suspected. <br>
Risk: The skill depends on a third-party API service and requires a sensitive credential to retrieve live Taobao and Tmall data. <br>
Mitigation: Install only when the publisher and service are trusted, store JUST_ONE_API_TOKEN in the agent environment, and avoid pasting the token into chat messages or screenshots. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-taobao) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and API-backed JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses GET operations that require a JustOneAPI token and task-specific query parameters such as itemId, page, sort, userId, and shopId.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
