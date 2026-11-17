## Description:

Call GET /api/v1/google/search/mobile for Google SERP Search Mobile through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SEO analysts use this skill to call Just Serp API's Google mobile search endpoint, retrieve mobile-specific Google SERP data, and summarize ranking or result-layout information for a supplied search query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports that this skill handles the API key through command-line arguments.

Mitigation: Prefer using a version or wrapper that reads JUST_SERP_API_KEY directly from the environment, and avoid exposing command histories or logs that may contain credentials.

Risk: The release evidence reports that searches, locations, business identifiers, and SERP targets are sent to a third-party API.

Mitigation: Avoid sending precise location data, confidential queries, or sensitive business identifiers unless sharing them with Just Serp API is intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-search-mobile)
- [Just Serp API Homepage](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_search_mobile&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_search_mobile&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a query; optional Google search, localization, and result-filter parameters can be passed through query parameters.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
