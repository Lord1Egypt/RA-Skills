## Description: <br>
Call GET /api/v1/google/search/light for Google SERP Search Light through Just Serp API with query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query Just Serp API's Google SERP Search Light endpoint for essential Google search result data, including fast rank checks and high-volume monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and optional localization parameters are sent to Just Serp API. <br>
Mitigation: Avoid secrets, highly personal information, confidential business investigations, and sensitive location context in queries unless sharing them with Just Serp API is acceptable. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Pass JUST_SERP_API_KEY through the environment or command option and do not paste key values into chat messages, screenshots, or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justserpapi/justserpapi-google-search-light) <br>
- [Just Serp API project site](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_search_light&utm_content=project_link) <br>
- [Just Serp API documentation](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_search_light&utm_content=project_link) <br>
- [Generated operation reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown summary with endpoint details, command examples, and raw JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and sends search parameters to Just Serp API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
