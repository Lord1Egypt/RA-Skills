## Description: <br>
Call GET /api/instagram/get-user-detail/v1 for Instagram User Profile through JustOneAPI with username. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to retrieve basic Instagram profile metadata for a provided username through JustOneAPI, including follower, following, and post counts. It is suited for legitimate account metadata workflows where the user has a reason to query a specific handle. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retrieves Instagram profile metadata and can be misused for unauthorized monitoring or profiling. <br>
Mitigation: Use it only for legitimate lookups of specific usernames and avoid broad surveillance or profiling workflows. <br>
Risk: The JustOneAPI token is sensitive and this API sends it as a request query parameter. <br>
Mitigation: Provide the token through JUST_ONE_API_TOKEN or the helper's token argument, and avoid exposing token values in chat, logs, screenshots, or shared command history. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_user_detail&utm_content=project_link) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_user_detail&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, JSON] <br>
**Output Format:** [Markdown summary followed by raw JSON when appropriate] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a username; backend errors should include the operation ID and response payload.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
