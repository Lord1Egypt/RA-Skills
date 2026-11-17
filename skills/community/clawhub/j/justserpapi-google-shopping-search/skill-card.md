## Description:

Call GET /api/v1/google/shopping/search for Google SERP Shopping Search through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run Google Shopping searches through Just Serp API for product listings, prices, merchants, pricing research, and catalog monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping search terms, localization settings, and the Just Serp API key are sent to Just Serp API.

Mitigation: Install and run this skill only when that data sharing is acceptable, keep the API key out of chat messages and logs, and avoid sensitive personal, confidential business, or secret data in search queries.

Risk: The skill performs expected network API calls and may return raw backend error payloads.

Mitigation: Review backend payloads before sharing them externally and avoid including secrets or sensitive query details in troubleshooting transcripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-shopping-search)
- [Just Serp API Project Site](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_shopping_search&utm_content=project_link)
- [Just Serp API Documentation](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_shopping_search&utm_content=project_link)
- [Generated Operation Reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and sends query parameters to Just Serp API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
