## Description:

Call GET /api/v1/google/search for Google SERP Search through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and search analysis teams use this skill to retrieve Google SERP data from Just Serp API for keyword tracking, market checks, organic result review, ads, and knowledge panel analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Just Serp API key is passed through a command-line argument, where it may be locally exposed.

Mitigation: Use a limited-scope API key if available, avoid sensitive searches or precise personal location parameters, and prefer a release that reads the key directly from the environment.

## Reference(s):

- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_search&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_search&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown summary with raw JSON API response when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a query parameter; optional localization, language, paging, SafeSearch, and advanced Google search parameters are supported.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
