## Description: <br>
Call GET /api/weibo/get-user-post/v1 for Weibo User Published Posts through JustOneAPI with uid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve published Weibo posts for a specific UID through JustOneAPI. It supports account monitoring workflows by returning post text, media, and publish-time data from the documented endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required JustOneAPI token may be exposed through command arguments or query-string handling. <br>
Mitigation: Use a limited, revocable token, avoid pasting token values into chat or logs, and prefer a version that keeps credentials out of command arguments and URLs. <br>
Risk: The endpoint retrieves Weibo account published-post data, which may be sensitive or subject to legal and policy constraints. <br>
Mitigation: Use the skill only for legitimate, lawful account-monitoring purposes and avoid sharing raw command output when it contains sensitive data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-weibo-get-user-post) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_user_post&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JUST_ONE_API_TOKEN credential and a target Weibo uid; optional pagination inputs are page and sinceId.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
