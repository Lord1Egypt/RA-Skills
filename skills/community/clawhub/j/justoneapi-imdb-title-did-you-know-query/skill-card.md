## Description: <br>
Call GET /api/imdb/title-did-you-know-query/v1 for IMDb 'Did You Know' Insights through JustOneAPI with id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content teams use this skill to look up IMDb title 'Did You Know' insights, including trivia, through JustOneAPI by IMDb title ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent to the API as a URL query parameter, which can expose it in URL logs or telemetry. <br>
Mitigation: Keep the token in the JUST_ONE_API_TOKEN environment variable, avoid pasting it into chat or logs, and rotate it if URL logs or telemetry may have exposed it. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_did_you_know_query&utm_content=project_link) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_did_you_know_query&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-imdb-title-did-you-know-query) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, JSON] <br>
**Output Format:** [Markdown summary with optional raw JSON response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and an IMDb title ID; optional languageCountry controls locale.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
