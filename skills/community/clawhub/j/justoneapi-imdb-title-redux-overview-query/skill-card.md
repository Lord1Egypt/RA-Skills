## Description: <br>
Call GET /api/imdb/title-redux-overview-query/v1 for IMDb Redux Overview through JustOneAPI with id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call JustOneAPI's IMDb Redux Overview endpoint for a movie or TV title by IMDb ID, then summarize key title metadata and linked overview fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is passed to the helper and included as a query parameter in the API request. <br>
Mitigation: Use a scoped or low-privilege token when available, avoid sharing command output, URLs, or network logs, and rotate the token if a request URL may have been exposed. <br>
Risk: Backend errors may include payloads from the API service. <br>
Mitigation: Review error output before sharing it and redact any sensitive request, account, or token-related details. <br>


## Reference(s): <br>
- [JustOneAPI API Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_redux_overview_query&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_redux_overview_query&utm_content=project_link) <br>
- [ClawHub Skill Listing](https://clawhub.ai/justoneapi/justoneapi-imdb-title-redux-overview-query) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and an IMDb title id; optional languageCountry controls localization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
