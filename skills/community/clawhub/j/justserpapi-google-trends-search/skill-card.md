## Description:

Call GET /api/v1/google/trends/search for Google SERP Trends Search through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query Just Serp API's Google Trends search endpoint for interest-over-time, geographic breakdown, and related-query data for demand analysis and seasonal trend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, filters, and the Just Serp API key are sent to Just Serp API; the helper passes the API key on the command line.

Mitigation: Run in an environment where process arguments, command history, CI logs, and telemetry are not exposed, and rotate the key if exposure is suspected.

Risk: Backend errors such as invalid API keys, quota exhaustion, or upstream service failures can interrupt results.

Mitigation: Handle the returned backend payload and operation ID, and verify credentials and quota before relying on results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-trends-search)
- [Just Serp API Homepage](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_search&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_search&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Markdown summary with optional shell command and raw JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JUST_SERP_API_KEY and query parameters for a GET request to /api/v1/google/trends/search.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
