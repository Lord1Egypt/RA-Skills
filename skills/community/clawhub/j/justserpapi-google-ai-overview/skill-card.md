## Description: <br>
Call GET /api/v1/google/ai-overview for Google SERP Ai Overview through Just Serp API with url. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and search visibility teams use this skill to fetch Google AI Overview data from Just Serp API for a supplied AI Overview URL, then summarize generated summaries and cited sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted URLs are shared with Just Serp API and may expose private, internal, or sensitive resources. <br>
Mitigation: Avoid submitting private, internal, or sensitive URLs unless third-party processing by Just Serp API is acceptable. <br>
Risk: The skill requires a sensitive Just Serp API credential. <br>
Mitigation: Pass the key through JUST_SERP_API_KEY or the helper's --api-key argument and do not paste key values into chat messages, screenshots, or logs. <br>
Risk: The required Google AI Overview URL is transient and may expire quickly. <br>
Mitigation: Use a fresh ai_overview_url value and ask for a replacement when the backend returns an expiration or request failure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justserpapi/justserpapi-google-ai-overview) <br>
- [Just Serp API project site](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_ai_overview&utm_content=project_link) <br>
- [Just Serp API documentation](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_ai_overview&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown summary with raw JSON response and optional shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a transient Google AI Overview url parameter; no request body.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
