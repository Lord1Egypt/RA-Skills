## Description: <br>
Call GET /api/imdb/title-critics-review-summary-query/v1 for IMDb Critics Review Summary through JustOneAPI with id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to call JustOneAPI for IMDb critics review summary data by title id, then summarize review highlights for review analysis and title comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a query parameter and may appear in request URLs captured by logs, traces, screenshots, or error reports. <br>
Mitigation: Keep the token out of chat and shared logs, avoid publishing run output that may expose request URLs, and rotate the token if exposure is suspected. <br>
Risk: The skill sends IMDb title ids and optional locale preferences to JustOneAPI. <br>
Mitigation: Use the skill only when sharing those lookup inputs with JustOneAPI is acceptable for the user's workflow. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_critics_review_summary_query&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_critics_review_summary_query&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-imdb-title-critics-review-summary-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper calls one GET endpoint, requires a JustOneAPI token, and returns parsed JSON after the agent summarizes the endpoint-specific result.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
