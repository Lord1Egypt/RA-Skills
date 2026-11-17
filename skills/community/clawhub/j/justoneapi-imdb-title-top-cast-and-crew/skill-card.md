## Description:

Call GET /api/imdb/title-top-cast-and-crew/v1 for IMDb Top Cast and Crew through JustOneAPI with id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve IMDb title top cast and crew data through JustOneAPI for talent research and title enrichment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is sent in the URL query string, which can expose the credential in logs or telemetry.

Mitigation: Use a limited or disposable token when available, avoid sharing command logs, and rotate the token if request URLs may have been logged.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_top_cast_and_crew&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_top_cast_and_crew&utm_content=project_link)
- [ClawHub Skill Release](https://clawhub.ai/justoneapi/skills/justoneapi-imdb-title-top-cast-and-crew)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with command guidance and JSON API response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and an IMDb title id; supports optional languageCountry.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
