## Description: <br>
Call GET /api/douyin-xingtu/get-kol-cp-info/v1 for Douyin Creator Marketplace (Xingtu) Cost Performance Analysis through JustOneAPI with kolId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to call a JustOneAPI endpoint for Douyin Creator Marketplace creator cost performance data. It supports creator evaluation, campaign planning, and marketplace research using a required KOL ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JUST_ONE_API_TOKEN credential is sent to api.justoneapi.com and could be exposed if full request URLs, command lines, or error reports are logged. <br>
Mitigation: Use a limited-scope or disposable token when available, avoid logging full request URLs or command invocations with token values, and rotate the token if exposure is suspected. <br>
Risk: The skill returns backend JSON and backend error payloads for a specific KOL lookup, so downstream decisions can be affected by missing, stale, or failed API responses. <br>
Mitigation: Check the operation ID, endpoint path, KOL ID, HTTP status, and returned payload before using results for creator evaluation or campaign planning. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-get-kol-cp-info) <br>
- [JustOneAPI API Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_cp_info&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_cp_info&utm_content=project_link) <br>
- [Generated Operation Reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a kolId query parameter; accepts optional acceptCache.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
