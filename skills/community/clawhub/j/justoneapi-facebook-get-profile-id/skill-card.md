## Description: <br>
Call GET /api/facebook/get-profile-id/v1 for Facebook Get Profile ID through JustOneAPI with url. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to call a JustOneAPI endpoint that retrieves a unique Facebook profile ID from a supplied Facebook profile URL path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token and Facebook lookup input are sent to a third-party API provider. <br>
Mitigation: Use the skill only when the user trusts JustOneAPI with the token and lookup input. <br>
Risk: Command lines, logs, screenshots, or full request URLs may expose the API token. <br>
Mitigation: Keep token values out of shared messages and logs, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_get_profile_id&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_get_profile_id&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-facebook-get-profile-id) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the getProfileIdV1 operation on /api/facebook/get-profile-id/v1 and requires JUST_ONE_API_TOKEN plus the url query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
