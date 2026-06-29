## Description: <br>
Call GET /api/v1/google/immersive/product for Google SERP Immersive Product through Just Serp API with page_token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Google immersive product details, features, specifications, and seller information from Just Serp API for product research and merchandising analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Just Serp API key and sends product page_token values plus optional localization or seller pagination parameters to Just Serp API. <br>
Mitigation: Keep JUST_SERP_API_KEY in environment variables or trusted secret storage, avoid pasting it into chat or logs, and install only when intending to use Just Serp API. <br>
Risk: API use may consume Just Serp credits or fail when access, credits, or quota are insufficient. <br>
Mitigation: Confirm expected usage before execution and surface backend authentication, access, quota, or credit errors to the user. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/justserpapi-google-immersive-product) <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_immersive_product&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_immersive_product&utm_content=project_link) <br>
- [Just Serp API Base URL](https://api.justserpapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON when results are returned] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a page_token; optional query parameters include country, language, stores, and sori.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
