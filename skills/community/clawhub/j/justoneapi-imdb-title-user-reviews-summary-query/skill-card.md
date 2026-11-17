## Description:

Call GET /api/imdb/title-user-reviews-summary-query/v1 for IMDb User Reviews Summary through JustOneAPI with id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve IMDb title user review summary data from JustOneAPI for audience sentiment analysis by IMDb title ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a JustOneAPI token and the security evidence flags token handling as exposure-prone.

Mitigation: Use a narrowly scoped or disposable token when available, avoid environments that log command lines or full request URLs, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-imdb-title-user-reviews-summary-query)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_user_reviews_summary_query&utm_content=project_link)
- [Just One API dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_user_reviews_summary_query&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and an IMDb title ID; optional languageCountry controls language and country preferences.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
