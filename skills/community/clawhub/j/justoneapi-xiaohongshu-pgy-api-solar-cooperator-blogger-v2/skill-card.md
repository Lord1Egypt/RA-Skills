## Description: <br>
Call GET /api/xiaohongshu-pgy/api/solar/cooperator/blogger/v2/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Search through JustOneAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to call a JustOneAPI endpoint that searches Xiaohongshu Creator Marketplace creators by keyword, audience filters, follower range, gender, and content tags for discovery, comparison, and shortlist building. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token can be exposed through command lines, full request URLs, shell history, process listings, or request logs. <br>
Mitigation: Use the skill only on trusted machines, avoid logging commands or full request URLs, prefer a limited-scope and short-lived token, and rotate the token if exposure is possible. <br>
Risk: The skill sends creator search queries and filters to the JustOneAPI backend. <br>
Mitigation: Review search terms and filters before execution and avoid including sensitive or unnecessary data in query parameters. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_cooperator_blogger_v2&utm_content=project_link) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_cooperator_blogger_v2&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-api-solar-cooperator-blogger-v2) <br>
- [generated/operations.md](artifact/generated/operations.md) <br>
- [generated/operations.json](artifact/generated/operations.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [A concise endpoint summary followed by raw JSON returned from the JustOneAPI backend.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; request parameters are sent as query arguments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
