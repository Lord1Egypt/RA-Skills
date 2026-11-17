## Description:

Call GET /api/imdb/main-search-query/v1 for IMDb Keyword Search through JustOneAPI with searchTerm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search IMDb through JustOneAPI by keyword and retrieve matched results, metadata, and ranking signals for entity discovery or entertainment research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper passes the JustOneAPI token on the command line and sends it as a request URL query parameter, which may expose it through process listings, logs, shell history, or captured URLs.

Mitigation: Use a limited or easily rotated JustOneAPI token, avoid logging full commands or URLs, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_main_search_query&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_main_search_query&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-imdb-main-search-query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown summary with optional shell command and raw JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a searchTerm query parameter; optional filters include type, limit, and languageCountry.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
