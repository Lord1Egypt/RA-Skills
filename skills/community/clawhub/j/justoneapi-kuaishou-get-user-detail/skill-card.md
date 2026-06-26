## Description: <br>
Call GET /api/kuaishou/get-user-detail/v1 for Kuaishou User Profile through JustOneAPI with userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch Kuaishou user profile data through JustOneAPI for creator research, creator profile building, and monitoring account status or audience growth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token and sends both token and userId as URL query parameters. <br>
Mitigation: Keep JUST_ONE_API_TOKEN local, avoid pasting it into chat, and redact full request URLs from logs, screenshots, and support tickets. <br>
Risk: The endpoint returns Kuaishou profile data that can include account metadata, audience metrics, and verification-related fields. <br>
Mitigation: Use the data only for legitimate profile research or monitoring needs, and avoid sharing raw profile payloads beyond the intended workflow. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_user_detail&utm_content=project_link) <br>
- [Kuaishou User Profile API on ClawHub](https://clawhub.ai/justoneapi/justoneapi-kuaishou-get-user-detail) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a Kuaishou userId; successful calls return parsed JSON from the JustOneAPI endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
