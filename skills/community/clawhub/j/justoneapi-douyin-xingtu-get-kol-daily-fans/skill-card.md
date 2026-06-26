## Description: <br>
Call GET /api/douyin-xingtu/get-kol-daily-fans/v1 for Douyin Creator Marketplace (Xingtu) Follower Growth Trend through JustOneAPI with endDate, kolId, and startDate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to call a focused JustOneAPI endpoint for Douyin Creator Marketplace follower growth trend data. It supports creator evaluation, campaign planning, and marketplace research for a specified KOL and date range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a query parameter and may appear in command history, logs, or copied request URLs. <br>
Mitigation: Use a limited-scope token if available, avoid sharing token-bearing commands or URLs, and rotate the token if it may have been exposed. <br>
Risk: The skill makes outbound HTTPS calls to api.justoneapi.com using user-provided lookup parameters. <br>
Mitigation: Install and run it only in environments where outbound calls to JustOneAPI are approved, and review parameters before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-get-kol-daily-fans) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_daily_fans&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_daily_fans&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with raw JSON output when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token, KOL ID, start date, and end date; optional cache acceptance can be passed as a query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
