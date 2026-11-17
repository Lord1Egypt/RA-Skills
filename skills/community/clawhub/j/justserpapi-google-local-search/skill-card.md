## Description:

Call GET /api/v1/google/local/search for Google SERP Local Search through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Just Serp API's Google local search endpoint for business listings, ratings, and contact details using a required search query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper requires a Just Serp API key and passes it through --api-key, which can expose credentials in logged or visible process command lines.

Mitigation: Run it only where process command lines are not exposed or logged, and prefer a version that reads JUST_SERP_API_KEY directly from the environment.

Risk: The skill makes outbound requests to api.justserpapi.com with user-supplied local search parameters.

Mitigation: Use intended query and location filters, and review API responses before relying on local lead generation or competitor research outputs.

## Reference(s):

- [Just Serp API homepage](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_local_search&utm_content=project_link)
- [Just Serp API docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_local_search&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justserpapi/skills/justserpapi-google-local-search)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown summary followed by raw JSON from the Just Serp API helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_SERP_API_KEY; calls GET /api/v1/google/local/search with query parameters.]

## Skill Version(s):

1.0.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
