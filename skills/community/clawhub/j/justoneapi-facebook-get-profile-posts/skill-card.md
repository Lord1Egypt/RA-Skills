## Description: <br>
Call GET /api/facebook/get-profile-posts/v1 for Facebook Get Profile Posts through JustOneAPI with profileId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve public posts from a Facebook profile through JustOneAPI when given a Facebook profile ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a request URL query parameter and may be exposed through logs, screenshots, or error output. <br>
Mitigation: Keep JUST_ONE_API_TOKEN private, avoid sharing full request URLs or raw error logs, and rotate the token if exposure is suspected. <br>
Risk: The skill sends Facebook profile lookup requests through JustOneAPI. <br>
Mitigation: Install and use it only if JustOneAPI is trusted with the API token and requested Facebook profile identifiers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-facebook-get-profile-posts) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_get_profile_posts&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with JSON response data and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; accepts profileId and optional cursor query parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
