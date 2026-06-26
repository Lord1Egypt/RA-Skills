## Description: <br>
Call GET /api/beike/community/list/v1 for Beike Community List through JustOneAPI with cityId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query JustOneAPI's Beike community-list endpoint for communities in a specified city. It supports comparing community names, identifiers, average listing prices, and historical price trends returned by the API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token is sent in the URL query string, which can be exposed through shared URLs or logs. <br>
Mitigation: Use a minimally scoped JustOneAPI token when available, avoid sharing full request URLs or error logs, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-beike-community-list) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike_community_list&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike_community_list&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON from the API when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; cityId is required, with optional condition and limitOffset query parameters.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
