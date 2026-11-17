## Description:

Call GET /api/v1/google/scholar/profiles for Google SERP Scholar Profiles through Just Serp API with mauthors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Google Scholar profiles through Just Serp API, using the required mauthors query to retrieve researcher profile results, affiliations, citation counts, and pagination tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google Scholar profile searches and query parameters are sent to Just Serp API.

Mitigation: Install and use the skill only when sending those searches to Just Serp API with your own API key is acceptable for the intended workflow.

Risk: The documented command passes the API key as a process argument, which can expose it on shared machines, CI systems, or monitored environments.

Mitigation: Prefer a revised helper that reads JUST_SERP_API_KEY directly from the environment, and avoid exposing API keys in chat messages, screenshots, logs, or process listings.

## Reference(s):

- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_profiles&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_profiles&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-scholar-profiles)
- [ClawHub Publisher Profile](https://clawhub.ai/user/justserpapi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_SERP_API_KEY; uses mauthors as the required query parameter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
