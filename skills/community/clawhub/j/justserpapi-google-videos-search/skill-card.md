## Description:

Call GET /api/v1/google/videos/search for Google SERP Videos Search through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Just Serp API for Google video search results by search term, with optional localization, language, time, SafeSearch, and pagination filters. It supports video SEO and content monitoring workflows that need titles, sources, dates, and related Google Videos result data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search queries and optional filters to Just Serp API.

Mitigation: Use it only for queries and filters appropriate to share with Just Serp API.

Risk: The skill requires a Just Serp API key.

Mitigation: Keep JUST_SERP_API_KEY in the environment and avoid pasting key values into chat messages, screenshots, or logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-videos-search)
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_videos_search&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_videos_search&utm_content=project_link)
- [Generated Operations Reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with an inline bash command and JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY; search queries and optional filters are sent to Just Serp API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
