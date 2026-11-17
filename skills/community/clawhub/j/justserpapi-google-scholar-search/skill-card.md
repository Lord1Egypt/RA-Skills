## Description:

Call GET /api/v1/google/scholar/search for Google SERP Scholar Search through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Just Serp API's Google Scholar search endpoint for academic search results, including papers, patents, legal documents, citations, year filters, versions, and cited-by links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper accepts JUST_SERP_API_KEY through a command-line argument, which can expose the key through process command-line metadata.

Mitigation: Run the skill only in a trusted local environment, avoid shared hosts or logged CI shells, and rotate the API key if it may have appeared in process logs or monitoring telemetry.

Risk: Scholar search queries are sent to Just Serp API.

Mitigation: Use the skill only when sending the intended search terms to Just Serp API is acceptable for the user's data-handling requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-scholar-search)
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_search&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_search&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_SERP_API_KEY; the helper returns parsed JSON on success and structured JSON error payloads on failure.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
