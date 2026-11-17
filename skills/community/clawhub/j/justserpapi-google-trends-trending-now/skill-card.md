## Description:

Call GET /api/v1/google/trends/trending-now for Google SERP Trends Trending Now through Just Serp API with geo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call the Just Serp API Google Trends Trending Now endpoint for region-scoped breaking-trend monitoring and editorial planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Just Serp API key can be exposed through local process command lines when passed with --api-key.

Mitigation: Review before installing in API-key-sensitive environments, prefer a release that reads JUST_SERP_API_KEY directly from the environment, and rotate the key if command logging or process monitoring may have captured it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-trends-trending-now)
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_trending_now&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_trending_now&utm_content=project_link)
- [Just Serp API Base URL](https://api.justserpapi.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a geo query parameter; optional hours and language query parameters are supported.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
