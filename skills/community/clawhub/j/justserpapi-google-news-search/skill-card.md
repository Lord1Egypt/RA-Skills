## Description:

Call GET /api/v1/google/news/search for Google SERP News Search through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Just Serp API's Google News search endpoint for headlines and source metadata for media monitoring or news aggregation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented command passes the Just Serp API key through a command-line argument, which can expose it through shell history, process monitoring, or logs.

Mitigation: Prefer a version that reads JUST_SERP_API_KEY directly from the process environment; avoid pasting key values into chat or logs and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/justserpapi/skills/justserpapi-google-news-search)
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_news_search&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_news_search&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses query parameters for Google News search and requires JUST_SERP_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
