## Description:

Call GET /api/imdb/title-contribution-questions/v1 for IMDb Contribution Questions through JustOneAPI with id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up IMDb title contribution question data for title metadata review and data maintenance workflows. The skill requires a JustOneAPI token and an IMDb title id.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be placed in request URLs, which may expose it through logs or telemetry.

Mitigation: Use a low-scope, revocable token, avoid sharing token values in chat or logs, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_contribution_questions&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-imdb-title-contribution-questions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional raw JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the titleContributionQuestions operation on /api/imdb/title-contribution-questions/v1 and preserves user-provided lookup parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
