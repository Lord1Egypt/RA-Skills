## Description:

Call GET /api/imdb/title-extended-details-query/v1 for IMDb Extended Details through JustOneAPI with id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve IMDb title extended details, including title information, images, and genres, for title enrichment and catalog research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command arguments or full request URL logging.

Mitigation: Run only in environments where process arguments and request URLs are not broadly logged, avoid sharing diagnostics or command output, and rotate the token if it may have been captured.

Risk: The token may have billing, quota, or account-sensitive access.

Mitigation: Review the token scope before installation and use the least-privileged token available for the IMDb endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-imdb-title-extended-details-query)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_extended_details_query&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_extended_details_query&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Short endpoint-specific summary followed by raw JSON from the API when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and an IMDb title id; optional languageCountry controls language and country preferences.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
