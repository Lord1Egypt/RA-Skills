## Description: <br>
Call GET /api/v1/google/scholar/author for Google SERP Scholar Author through Just Serp API with author_id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to call Just Serp API's Google Scholar author endpoint and retrieve author profile data, publications, citation metrics, and research interests for researcher analysis and academic profiling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Just Serp API credential. <br>
Mitigation: Provide JUST_SERP_API_KEY through the documented environment or command argument flow, and do not paste key values into chat messages, screenshots, or logs. <br>
Risk: The skill makes outbound requests to Just Serp API and may return backend error payloads. <br>
Mitigation: Review the displayed permissions, required credentials, and network destination before installation, and inspect backend error payloads before sharing them. <br>


## Reference(s): <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_author&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_author&utm_content=project_link) <br>
- [Just Serp API Base URL](https://api.justserpapi.com) <br>
- [ClawHub skill page](https://clawhub.ai/justserpapi/justserpapi-google-scholar-author) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and an author_id query parameter.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
