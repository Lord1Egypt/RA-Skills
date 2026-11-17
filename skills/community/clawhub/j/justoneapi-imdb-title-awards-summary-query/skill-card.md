## Description:

Call GET /api/imdb/title-awards-summary-query/v1 for IMDb Awards Summary through JustOneAPI with id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query JustOneAPI for IMDb title awards summary data, including nominations, for title benchmarking and awards research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill handles the JustOneAPI token in exposed places.

Mitigation: Use a narrowly scoped token that can be rotated, avoid sharing command logs or process listings, and review the skill before installing when the token has paid quota or broad account access.

Risk: Backend errors may include request or response details.

Mitigation: Review error output before sharing it and remove tokens, URLs, or account-specific details from logs and reports.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_awards_summary_query&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_awards_summary_query&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-imdb-title-awards-summary-query)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and an IMDb title id; optional languageCountry controls localization.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
