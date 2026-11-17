## Description:

Call GET /api/v1/google/search/light for Google SERP Search Light through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Just Serp API's light Google search endpoint with a required query and optional localization, filtering, and paging parameters. It supports fast retrieval of essential SERP data for monitoring and rank-check workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and localization parameters are sent to Just Serp API.

Mitigation: Use only queries and location context that are appropriate to share with the API provider.

Risk: The skill requires a JUST_SERP_API_KEY to call the endpoint.

Mitigation: Provide the key through the expected environment or command argument and avoid pasting secret values into chat messages, screenshots, or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justserpapi/skills/justserpapi-google-search-light)
- [Just Serp API project site](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_search_light&utm_content=project_link)
- [Just Serp API documentation](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_search_light&utm_content=project_link)
- [Generated operation reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, JSON, Markdown]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a query parameter; optional parameters control location, language, paging, raw HTML, SafeSearch, and Google result filters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
