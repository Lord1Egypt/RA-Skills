## Description:

Call GET /api/v1/google/shorts/search for Google SERP Shorts Search through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query the Just Serp API for Google Shorts search results, including video metadata and rankings for short-form content tracking and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Just Serp API key is passed on the command line and may be exposed through local process logs or monitoring.

Mitigation: Review before installing in monitored or shared environments, prefer an implementation that reads JUST_SERP_API_KEY directly from the environment, and rotate the key if exposure is suspected.

Risk: The skill can return raw Google result HTML when the html parameter is enabled.

Mitigation: Use the html option only when raw page content is needed, and review returned content before storing or sharing it.

## Reference(s):

- [Just Serp API homepage](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_shorts_search&utm_content=project_link)
- [Just Serp API docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_shorts_search&utm_content=project_link)
- [Just Serp API base URL](https://api.justserpapi.com)
- [ClawHub skill page](https://clawhub.ai/justserpapi/skills/justserpapi-google-shorts-search)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_SERP_API_KEY; the required query parameter is sent as a query argument.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
