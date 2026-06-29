## Description: <br>
Call GET /api/v1/google/shorts/search for Google SERP Shorts Search through Just Serp API with query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query Just Serp API for Google Shorts search results, localized search parameters, video metadata, and rankings for short-form content tracking and trend analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Just Serp API key. <br>
Mitigation: Provide JUST_SERP_API_KEY through the environment or --api-key argument, and do not paste key values into chat messages, screenshots, or logs. <br>
Risk: The helper sends user-supplied search parameters to the Just Serp API service. <br>
Mitigation: Review query and localization parameters before execution, and avoid sending sensitive or confidential search terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justserpapi/justserpapi-google-shorts-search) <br>
- [Just Serp API project site](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_shorts_search&utm_content=project_link) <br>
- [Just Serp API documentation](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_shorts_search&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with inline shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY; documented usage returns a short endpoint-specific summary before raw JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
