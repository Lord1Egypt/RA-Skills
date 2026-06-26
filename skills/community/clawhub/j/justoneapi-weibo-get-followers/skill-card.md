## Description: <br>
Call GET /api/weibo/get-followers/v1 for Weibo User Followers through JustOneAPI with uid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to call JustOneAPI's Weibo follower endpoint for a specified UID and summarize follower data, profile metadata, and verification signals for network analysis or creator research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a JustOneAPI token and requested Weibo UID to JustOneAPI, and the security summary notes that token handling can expose credentials in command arguments and request URLs. <br>
Mitigation: Use a scoped, rotatable token; run the command only on trusted systems; avoid logging command lines or URLs; prefer a version that reads the token directly from the environment and sends it through a non-URL authorization mechanism. <br>


## Reference(s): <br>
- [Generated Weibo User Followers operations](generated/operations.md) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_followers&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_followers&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command usage and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and uid; optional page parameter defaults to 1.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
