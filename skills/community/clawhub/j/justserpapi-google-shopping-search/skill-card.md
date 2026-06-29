## Description: <br>
Call GET /api/v1/google/shopping/search for Google SERP Shopping Search through Just Serp API with query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Just Serp API's Google Shopping search endpoint and retrieve product listings, prices, and merchant data for pricing research and catalog monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends JUST_SERP_API_KEY and user-provided shopping search parameters to Just Serp API. <br>
Mitigation: Use the skill only when Just Serp API is trusted for the API key and search terms; keep JUST_SERP_API_KEY out of chat, screenshots, and shared logs. <br>
Risk: Optional raw HTML requests may return upstream search-result HTML alongside structured data. <br>
Mitigation: Request raw HTML only when needed and treat returned HTML as untrusted data for review or downstream processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justserpapi/justserpapi-google-shopping-search) <br>
- [Just Serp API project site](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_shopping_search&utm_content=project_link) <br>
- [Just Serp API documentation](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_shopping_search&utm_content=project_link) <br>
- [Generated operation reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, JSON] <br>
**Output Format:** [Markdown summary followed by raw JSON from the Just Serp API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a query parameter; optional query parameters control localization, filtering, pagination, SafeSearch, and raw HTML inclusion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
