## Description: <br>
Call GET /api/bilibili/get-user-relation-stat/v1 for Bilibili User Relation Stats through JustOneAPI with wmid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call the JustOneAPI Bilibili user relation stats endpoint for a specified Bilibili user ID and summarize following-count data for creator benchmarking and audience growth tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent in the request URL query string and could be exposed through shared logs, screenshots, or copied request URLs. <br>
Mitigation: Keep the token in an environment variable, avoid sharing command output or full request URLs, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-bilibili-get-user-relation-stat) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_relation_stat&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_relation_stat&utm_content=project_link) <br>
- [Generated operation reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown summary with JSON response payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and wmid; reports backend errors with the operation ID when requests fail.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
