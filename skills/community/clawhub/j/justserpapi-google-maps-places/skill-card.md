## Description: <br>
Call GET /api/v1/google/maps/places for Google SERP Maps Places through Just Serp API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call the Just Serp API Google Maps Places endpoint and retrieve place details, contact details, and business information for local data enrichment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Just Serp API key, which is sensitive credential material. <br>
Mitigation: Provide the key through JUST_SERP_API_KEY or the helper's --api-key argument, and do not paste key values into chat messages, screenshots, or logs. <br>
Risk: API calls may fail because of invalid credentials, insufficient credits, quota limits, service errors, or network failures. <br>
Mitigation: Check the returned status and backend payload, preserve the operation ID mapsPlaces in error reports, and retry or adjust credentials and quota outside the skill. <br>
Risk: Using broad or incorrect place_id, data_id, or country parameters can return irrelevant place details. <br>
Mitigation: Ask for missing identifiers before calling the helper and keep user-provided IDs and country filters unchanged. <br>


## Reference(s): <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_places&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_places&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justserpapi/justserpapi-google-maps-places) <br>
- [Publisher profile](https://clawhub.ai/user/justserpapi) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with raw JSON API response and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the mapsPlaces operation for GET /api/v1/google/maps/places and requires JUST_SERP_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
