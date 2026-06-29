## Description: <br>
Call GET /api/v1/web/markdown for Web Crawling Markdown through Just Serp API with url. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit a webpage URL to Just Serp API and receive crawl output suitable for readable extraction, documentation workflows, and LLM input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Just Serp API credential. <br>
Mitigation: Provide the key through JUST_SERP_API_KEY or the helper's API-key argument, and do not paste key values into chat messages, screenshots, or logs. <br>
Risk: Requested URLs are sent to a third-party API service and may disclose private, signed, account-specific, localhost, or internal-network URLs. <br>
Mitigation: Avoid submitting sensitive URLs unless the provider's data-handling terms and the user's authorization have been reviewed. <br>
Risk: API failures, invalid credentials, insufficient credits, or upstream service errors can prevent successful crawling. <br>
Mitigation: Surface the operation ID, status, and backend payload so the user can distinguish parameter, quota, authentication, and provider-side issues. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justserpapi/justserpapi-web-markdown) <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_markdown&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_markdown&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with raw JSON from the API helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a user-provided URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
