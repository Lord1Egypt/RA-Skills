## Description:

Call GET /api/v1/google/maps/search for Google SERP Maps Search through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query Just Serp API for Google Maps search results, including business listings, ratings, contact data, coordinates, and localized place discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, optional coordinates, place IDs, and localization parameters are sent to Just Serp API.

Mitigation: Avoid submitting sensitive search terms or location data unless that disclosure is acceptable for the use case.

Risk: The helper accepts the API key as a command-line argument, which can expose credentials through shell history, tracing, or process logging.

Mitigation: Use a scoped or rotated JUST_SERP_API_KEY, avoid shell tracing and command logging, and prefer environment-based credential handling where possible.

Risk: Quota, credential, or upstream API errors can affect availability and result completeness.

Mitigation: Handle 401, 403, and 500 responses explicitly and review backend payloads before relying on results.

## Reference(s):

- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_search&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_search&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-maps-search)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown summary with optional raw JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a query parameter; optional parameters support localization, coordinates, place IDs, filters, and pagination.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
