## Description:

Call GET /api/imdb/title-release-expectation-query/v1 for IMDb Release Expectation through JustOneAPI with id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to look up IMDb title release expectation data by IMDb ID, including production status, release dates, and anticipation signals for release monitoring or title research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a JustOneAPI token that may be exposed through process listings or URL logs.

Mitigation: Use a narrowly scoped or revocable token, avoid running commands on shared machines, do not share logs containing request URLs, and rotate the token if exposure is suspected.

Risk: A token with paid quota or broad account access can create account or cost exposure if misused.

Mitigation: Review the skill before installation and use tokens with the minimum practical quota and permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-imdb-title-release-expectation-query)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_release_expectation_query&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_release_expectation_query&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the JUST_ONE_API_TOKEN environment variable and requires an IMDb title ID.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
