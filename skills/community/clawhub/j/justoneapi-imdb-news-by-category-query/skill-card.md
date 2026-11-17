## Description:

Call GET /api/imdb/news-by-category-query/v1 for IMDb News by Category through JustOneAPI with category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve IMDb news by category from JustOneAPI for media monitoring and news research. It supports TOP, MOVIE, TV, and CELEBRITY categories, with an optional language and country preference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is sent as a query parameter and may be exposed in logs or monitoring systems.

Mitigation: Use a scoped or low-quota token, avoid pasting token values into chat or logs, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_news_by_category_query&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-imdb-news-by-category-query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, JSON, guidance]

**Output Format:** [Markdown summary followed by raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a category query parameter; languageCountry defaults to en_US.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
