## Description:

Call GET /api/v1/google/finance/search for Google SERP Finance Search through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Just Serp API's Google Finance search endpoint for market summaries, company details, and related finance results by query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required API key can be exposed locally when passed as a command-line argument.

Mitigation: Prefer a version or wrapper that reads JUST_SERP_API_KEY directly from a protected environment or secret channel, and avoid logging commands that include credentials.

Risk: The skill makes external network requests to the Just Serp API endpoint.

Mitigation: Constrain runtime network egress to the Just Serp API endpoint and review backend error payloads before relying on results.

## Reference(s):

- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_finance_search&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_finance_search&utm_content=project_link)
- [Just Serp API Base URL](https://api.justserpapi.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the financeSearch operation with required query input and optional html and language query parameters.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
