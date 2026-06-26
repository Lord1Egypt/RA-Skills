## Description: <br>
Call GET /api/imdb/title-chart-rankings/v1 for IMDb Chart Rankings through JustOneAPI with rankingsChartType. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call JustOneAPI's IMDb chart rankings endpoint and retrieve Top 250 movie or TV ranking data for monitoring and title benchmarking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a URL query parameter, which may appear in request URLs, logs, screenshots, or browser history. <br>
Mitigation: Use a scoped or revocable token when available, avoid sharing full request URLs or logs, and rotate the token if exposure is suspected. <br>
Risk: The skill executes network requests to JustOneAPI and returns backend payloads, so results depend on the external service and the supplied token. <br>
Mitigation: Install only when the publisher and service are trusted, and review backend error payloads before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-imdb-title-chart-rankings) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_chart_rankings&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_chart_rankings&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; required query scope is rankingsChartType.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
