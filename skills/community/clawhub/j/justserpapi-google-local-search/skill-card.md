## Description: <br>
Call GET /api/v1/google/local/search for Google SERP Local Search through Just Serp API with query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Google local search data such as business listings, ratings, and contact details through Just Serp API for local lead generation and competitor research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Just Serp API key and uses that account's quota. <br>
Mitigation: Store the key in the documented JUST_SERP_API_KEY environment variable and avoid pasting the key into chat, screenshots, or logs. <br>
Risk: Search queries, locations, and filters are submitted to Just Serp API. <br>
Mitigation: Install and use the skill only when you trust Just Serp API with the submitted searches and locations. <br>


## Reference(s): <br>
- [Just Serp API Project Site](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_local_search&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_local_search&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/justserpapi-google-local-search) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/justserpapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the JUST_SERP_API_KEY environment variable and sends query parameters to the Just Serp API local search endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
