## Description: <br>
Call GET /api/douyin-xingtu/get-kol-info/v1 for Douyin Creator Marketplace (Xingtu) Creator Profile through JustOneAPI with kolId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and campaign analysts use this skill to fetch Douyin Creator Marketplace creator profile data by KOL ID for influencer vetting, benchmark analysis, and campaign planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a query parameter and may be captured in command histories, request URLs, proxy logs, or telemetry. <br>
Mitigation: Keep the token in JUST_ONE_API_TOKEN, avoid pasting token values into chats or logs, prefer a scoped or revocable token, and rotate it if exposure is possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-get-kol-info) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_info&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_info&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN; endpoint inputs include kolId plus optional platformChannel and acceptCache query parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
