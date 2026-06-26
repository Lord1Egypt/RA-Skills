## Description: <br>
Call GET /api/imdb/title-details-query/v1 for IMDb Details through JustOneAPI with id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up IMDb title details from JustOneAPI by IMDb id, optionally selecting a language and country preference. It supports title research and catalog enrichment by returning metadata, release information, and cast details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent in the request URL and could be exposed through shared command lines, logs, screenshots, or captured URLs. <br>
Mitigation: Use a rotatable token, avoid sharing logs or screenshots that include request URLs, and rotate the token if URL exposure is suspected. <br>
Risk: Lookup requests and token values are sent to JustOneAPI. <br>
Mitigation: Install and use the skill only when the publisher and JustOneAPI service are trusted for the intended IMDb lookups. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-imdb-title-details-query) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_details_query&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_details_query&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with an optional Node.js shell command and JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and an IMDb title id; the API token is passed as a query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
