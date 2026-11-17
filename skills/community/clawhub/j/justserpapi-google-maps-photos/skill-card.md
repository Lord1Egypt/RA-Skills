## Description:

Call GET /api/v1/google/maps/photos for Google SERP Maps Photos through Just Serp API with data_id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call Just Serp API's Google Maps Photos endpoint with a Google Maps data_id, retrieve photo data and related metadata, and support visual location research or listing QA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented command passes the Just Serp API key as a process argument, which may expose it locally through process listings or logs.

Mitigation: Prefer a version that reads JUST_SERP_API_KEY directly from the environment or another protected secret source; avoid pasting API keys into chat messages, screenshots, or logs.

## Reference(s):

- [Google SERP Maps Photos API on ClawHub](https://clawhub.ai/justserpapi/skills/justserpapi-google-maps-photos)
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_photos&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_photos&utm_content=project_link)
- [Generated Google SERP Maps Photos Operations](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, JSON, Guidance]

**Output Format:** [Markdown summary with endpoint details and raw JSON API response when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_SERP_API_KEY; the main operation is mapsPhotos for /api/v1/google/maps/photos.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
