## Description:

Call GET /api/imdb/title-critics-review-summary-query/v1 for IMDb Critics Review Summary through JustOneAPI with id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI's IMDb critics review summary endpoint for a title id and summarize review highlights for review analysis and title comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token and IMDb lookup ids are sent to api.justoneapi.com, and token values can leak through URL/query or command-line handling into logs, process views, shell history, proxy logs, or copied URLs.

Mitigation: Use a restricted or revocable token, avoid sharing command lines or logs from runs, and rotate the token if it may have been exposed.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_critics_review_summary_query&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_critics_review_summary_query&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-imdb-title-critics-review-summary-query)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown summary with optional raw JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; uses id as the required IMDb lookup parameter and languageCountry as an optional locale parameter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
