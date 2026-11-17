## Description:

Call GET /api/v1/google/maps/places for Google SERP Maps Places through Just Serp API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to call Just Serp API's Google Maps place-details endpoint, using place or data identifiers to retrieve contact and business information for directories, place lookup, or local app data sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Just Serp API key and may expose that credential if command arguments, shell tracing, or process logs are captured.

Mitigation: Pass the key from JUST_SERP_API_KEY, avoid logging command invocations with secrets, and rotate the key if it may have been exposed.

Risk: Calls are made to the documented Just Serp API endpoint and can fail when the API key is invalid or account quota is exhausted.

Mitigation: Confirm API access before operational use and handle authentication, quota, and upstream error payloads in the agent response.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-maps-places)
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_places&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_places&utm_content=project_link)
- [Just Serp API Base URL](https://api.justserpapi.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with inline shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JUST_SERP_API_KEY and optional query parameters place_id, data_id, and country.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
