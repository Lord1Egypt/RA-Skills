## Description: <br>
Call GET /api/imdb/title-box-office-summary/v1 for IMDb Box Office Summary through JustOneAPI with id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve IMDb title box-office summary data through JustOneAPI by IMDb ID. It supports revenue tracking and title comparison by summarizing grosses and related performance indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a query parameter and could be exposed in request URLs, logs, screenshots, shell history, or error traces. <br>
Mitigation: Use a dedicated, revocable token from an environment variable or secret store, avoid logging full request URLs, and rotate the token if exposure is suspected. <br>
Risk: The skill depends on an external JustOneAPI endpoint and may return backend errors or unavailable data for a requested IMDb ID. <br>
Mitigation: Ask for missing required parameters before execution, preserve the supplied IMDb ID, and include the backend payload and operation ID when reporting errors. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_box_office_summary&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_box_office_summary&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-imdb-title-box-office-summary) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with optional raw JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN; accepts IMDb id and optional languageCountry.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
