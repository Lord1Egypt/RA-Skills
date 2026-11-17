## Description:

Call GET /api/v1/google/maps/posts for Google SERP Maps Posts through Just Serp API with data_id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve Google Maps business post data through the Just Serp API. It supports local business monitoring and promotion tracking when the caller has a data_id and a JUST_SERP_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper passes the Just Serp API key through command-line arguments, where it can be exposed locally.

Mitigation: Prefer a revised release that reads JUST_SERP_API_KEY directly from the environment or a secret store, and restrict outbound access to api.justserpapi.com where possible.

## Reference(s):

- [Google SERP Maps Posts ClawHub page](https://clawhub.ai/justserpapi/skills/justserpapi-google-maps-posts)
- [Just Serp API homepage](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_posts&utm_content=project_link)
- [Just Serp API documentation](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_posts&utm_content=project_link)
- [Just Serp API base endpoint](https://api.justserpapi.com)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and the mapsPosts operation with a data_id query parameter.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
