## Description: <br>
Call GET /api/v1/google/search/mobile for Google SERP Search Mobile through Just Serp API with query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SEO analysts, and external agents use this skill to query Just Serp API for Google mobile search result data, including mobile-specific layouts and ranking signals, using a required search query and optional localization parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, optional location data, UULE values, business or entity identifiers, and raw HTML result requests are sent to Just Serp API. <br>
Mitigation: Use this skill only with data approved for that service and avoid secrets, personal data, regulated data, or confidential research terms unless that matches your data-handling requirements. <br>
Risk: The skill requires a Just Serp API key. <br>
Mitigation: Provide the key through JUST_SERP_API_KEY or the helper's API-key argument and do not paste credential values into chat messages, screenshots, or logs. <br>


## Reference(s): <br>
- [Just Serp API project site](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_search_mobile&utm_content=project_link) <br>
- [Just Serp API documentation](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_search_mobile&utm_content=project_link) <br>
- [Just Serp API base endpoint](https://api.justserpapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and the node runtime; uses operation searchMobile on /api/v1/google/search/mobile.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
