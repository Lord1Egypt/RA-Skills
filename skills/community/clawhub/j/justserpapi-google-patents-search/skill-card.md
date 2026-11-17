## Description:

Call GET /api/v1/google/patents/search for Google SERP Patents Search through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call the Just Serp API Google patents search endpoint for patent discovery and portfolio monitoring. It supports a required patent query plus optional pagination, sorting, localization, date, inventor, assignee, status, type, and litigation filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Just Serp API key can be exposed locally when passed as a command-line argument.

Mitigation: Use only a scoped key, avoid pasting key values into chat or logs, and prefer a version that reads the key from the environment or a secret manager.

Risk: The skill makes authenticated calls to api.justserpapi.com.

Mitigation: Install and use it only when you are comfortable granting access to a Just Serp API key for that service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-patents-search)
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_patents_search&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_patents_search&utm_content=project_link)
- [Just Serp API Base URL](https://api.justserpapi.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with an inline Node.js command and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a query parameter; the helper sends query parameters to /api/v1/google/patents/search.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
