## Description:

Call GET /api/v1/google/trends/autocomplete for Google SERP Trends Autocomplete through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Just Serp API for Google Trends autocomplete suggestions and topic IDs from a required search query, with optional language selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Query text is sent to Just Serp API, and the skill requires a Just Serp API key.

Mitigation: Use the skill only when sending the query to that provider is acceptable, avoid placing secrets in query text, and prefer a limited-scope or revocable API key when available.

## Reference(s):

- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_autocomplete&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_autocomplete&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-trends-autocomplete)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with raw JSON from the API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and sends query parameters to Just Serp API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
