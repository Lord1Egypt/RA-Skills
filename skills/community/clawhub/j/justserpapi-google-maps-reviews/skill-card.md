## Description:

Call GET /api/v1/google/maps/reviews for Google SERP Maps Reviews through Just Serp API with data_id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to fetch Google Maps reviews from Just Serp API for a specific data_id. It supports reputation analysis and review monitoring by summarizing ratings and reviewer metadata before returning raw JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Just Serp API key.

Mitigation: Provide JUST_SERP_API_KEY through the environment or --api-key and avoid pasting key values into chat messages, screenshots, or logs.

Risk: Responses can include third-party reviews and reviewer metadata.

Mitigation: Treat returned review data as third-party API data and avoid unnecessary logging or sharing.

## Reference(s):

- [Just Serp API Project Site](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_reviews&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_reviews&utm_content=project_link)
- [Google SERP Maps Reviews Operations](generated/operations.md)
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-maps-reviews)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with raw JSON and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and data_id; returned data may include third-party reviews and reviewer metadata.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
