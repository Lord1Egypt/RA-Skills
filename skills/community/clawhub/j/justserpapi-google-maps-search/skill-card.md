## Description: <br>
Call GET /api/v1/google/maps/search for Google SERP Maps Search through Just Serp API with query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business users use this skill to query Google Maps search data through Just Serp API for local market research, lead discovery, and place lookups using a required search query with optional localization parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Maps search terms, optional GPS coordinates, place IDs, and localization parameters are sent to Just Serp API using the user's API key. <br>
Mitigation: Avoid sensitive personal locations or confidential business searches unless third-party handling by Just Serp API is acceptable for the use case. <br>
Risk: The skill requires the JUST_SERP_API_KEY credential. <br>
Mitigation: Pass the key through the documented environment variable or command argument and do not include key values in chat messages, screenshots, or logs. <br>


## Reference(s): <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_search&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_search&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/justserpapi-google-maps-search) <br>
- [Generated Operations Reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with an executable Node.js command and JSON API responses] <br>
**Output Parameters:** [1D; mapsSearch requires query and accepts optional ll, domain, language, country, data, place_id, and page query parameters.] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY; requests send search and location parameters to Just Serp API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
