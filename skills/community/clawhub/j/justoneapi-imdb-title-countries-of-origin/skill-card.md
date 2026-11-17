## Description:

Call GET /api/imdb/title-countries-of-origin/v1 for IMDb Countries of Origin through JustOneAPI with id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up IMDb title countries of origin through JustOneAPI for catalog enrichment and regional content analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A JustOneAPI token is required and is sent as a query parameter to the documented endpoint, which can expose it through command history, process monitoring, proxy logs, or API logs.

Mitigation: Use a narrowly scoped token when available, do not paste token values into chat or logs, avoid recording command invocations that contain the token, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-imdb-title-countries-of-origin)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_countries_of_origin&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_countries_of_origin&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The endpoint requires an IMDb title id and a JustOneAPI token; languageCountry defaults to en_US when omitted.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
