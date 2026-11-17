## Description:

Call GET /api/v1/google/ai-overview for Google SERP Ai Overview through Just Serp API with url.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call Just Serp API's Google AI Overview endpoint for a supplied AI Overview URL and retrieve generated-summary and cited-source data for generative search visibility tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Google AI Overview lookup URLs to Just Serp API using the configured API key.

Mitigation: Install only when this data transfer is intended, keep JUST_SERP_API_KEY in the environment, and avoid pasting the key into chat, screenshots, or logs.

Risk: Provider handling of submitted URLs and returned responses may affect privacy, retention, or acceptable-use obligations.

Mitigation: Review Just Serp API provider terms before using the skill with sensitive or regulated lookup URLs.

## Reference(s):

- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_ai_overview&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_ai_overview&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-ai-overview)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown summary with raw JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a transient Google AI Overview URL.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
