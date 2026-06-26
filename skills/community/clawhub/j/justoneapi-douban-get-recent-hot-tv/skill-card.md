## Description: <br>
Call GET /api/douban/get-recent-hot-tv/v1 for Douban Movie Recent Hot Tv through JustOneAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to call JustOneAPI's Douban Movie recent hot TV endpoint for series discovery and trend monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token is placed in the request URL query string. <br>
Mitigation: Use a scoped or revocable JUST_ONE_API_TOKEN and avoid sharing token values in chat, screenshots, or logs. <br>
Risk: The skill depends on a third-party API service. <br>
Mitigation: Install only if you trust JustOneAPI and are comfortable sending requests to api.justoneapi.com. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/justoneapi/justoneapi-douban-get-recent-hot-tv) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_recent_hot_tv&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_recent_hot_tv&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JUST_ONE_API_TOKEN and supports an optional page query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
