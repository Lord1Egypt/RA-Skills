## Description: <br>
Call GET /api/imdb/title-contribution-questions/v1 for IMDb Contribution Questions through JustOneAPI with id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve IMDb title contribution question data by IMDb title ID for data maintenance workflows and title metadata review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token is sent in the request URL and may be exposed through logs, traces, screenshots, or copied URLs. <br>
Mitigation: Use a limited, revokable token; avoid sharing request URLs or logs; rotate the token if a URL containing it is exposed. <br>
Risk: The skill depends on a third-party API provider and a required JUST_ONE_API_TOKEN credential. <br>
Mitigation: Install only when the provider is trusted and keep the token in the environment rather than pasting credential values into chat messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-imdb-title-contribution-questions) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_contribution_questions&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_contribution_questions&utm_content=project_link) <br>
- [generated/operations.md](generated/operations.md) <br>
- [generated/operations.json](generated/operations.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and an IMDb title ID; optional languageCountry query parameter defaults to en_US.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
