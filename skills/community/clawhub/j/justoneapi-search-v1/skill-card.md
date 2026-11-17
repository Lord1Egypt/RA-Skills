## Description:

Call GET /api/search/v1 for Social Media Cross-Platform Search through JustOneAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call JustOneAPI's cross-platform social media search endpoint for trend research and monitoring across supported social and news sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command-line arguments and URL query parameters.

Mitigation: Use a narrowly scoped or short-lived token where possible, avoid sharing logs or process listings, and prefer a publisher update that reads secrets directly from the environment and authenticates via a header.

Risk: Search terms and filters are sent to api.justoneapi.com.

Mitigation: Avoid sensitive search terms unless this data sharing is acceptable for the intended use case.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_search_v1&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_search_v1&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown summary followed by JSON response data or JSON error payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the searchCrossPlatformV1 operation on GET /api/search/v1; no request body is documented.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
