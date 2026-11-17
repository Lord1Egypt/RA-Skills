## Description:

Call GET /api/imdb/title-did-you-know-query/v1 for IMDb 'Did You Know' Insights through JustOneAPI with id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to call JustOneAPI's IMDb titleDidYouKnowQuery endpoint for trivia and title insight enrichment by IMDb title ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is sent as a URL query parameter, which can expose it in logs, monitoring tools, or copied URLs.

Mitigation: Use a narrowly scoped, revocable token, avoid sharing token-bearing URLs or logs, and rotate the token if exposure is suspected.

Risk: The token may carry quota, billing, or account-level access.

Mitigation: Review token scope before installation and prefer credentials with limited account impact.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-imdb-title-did-you-know-query)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_did_you_know_query&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_did_you_know_query&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; accepts an IMDb title id and optional languageCountry.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
