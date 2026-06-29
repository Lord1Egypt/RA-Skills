## Description: <br>
Call GET /api/v1/google/maps/reviews for Google SERP Maps Reviews through Just Serp API with data_id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Google Maps reviews through Just Serp API for reputation analysis and review monitoring. It requires a Google Maps location data_id and can apply optional language, sorting, pagination, result count, and topic filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, data_id values, filters, and the configured API key are sent to the third-party Just Serp API service. <br>
Mitigation: Confirm JustSerpAPI is the intended provider, keep the key in JUST_SERP_API_KEY, and avoid private or regulated search inputs unless the provider and account terms are acceptable. <br>
Risk: The external API can fail because of invalid credentials, insufficient credits, quota exhaustion, upstream service errors, or network issues. <br>
Mitigation: Check the returned status and backend payload, preserve the operation ID for troubleshooting, and handle authentication or quota errors before retrying. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/justserpapi-google-maps-reviews) <br>
- [Just Serp API Homepage](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_reviews&utm_content=project_link) <br>
- [Just Serp API Documentation](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_reviews&utm_content=project_link) <br>
- [Just Serp API Base URL](https://api.justserpapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and sends endpoint parameters to Just Serp API.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
