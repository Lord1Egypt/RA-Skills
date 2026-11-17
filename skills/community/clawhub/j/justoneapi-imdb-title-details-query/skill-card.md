## Description:

Call GET /api/imdb/title-details-query/v1 for IMDb Details through JustOneAPI with id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to look up IMDb title details by IMDb ID through JustOneAPI. It supports title research and catalog enrichment by returning metadata, release information, and cast details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is passed through command-line arguments and query parameters, where it may be exposed in process metadata or service-side URL logs.

Mitigation: Use a narrowly scoped, revocable token, avoid sharing command output or logs that may contain URLs, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_details_query&utm_content=project_link)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_details_query&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with raw JSON returned after the endpoint-specific summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and an IMDb title id; optional languageCountry controls language and country preferences.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
