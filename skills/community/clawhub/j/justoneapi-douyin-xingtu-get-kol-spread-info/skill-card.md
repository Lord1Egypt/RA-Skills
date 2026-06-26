## Description: <br>
Call GET /api/douyin-xingtu/get-kol-spread-info/v1 for Douyin Creator Marketplace (Xingtu) Spread Metrics through JustOneAPI with kolId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call JustOneAPI's Douyin Creator Marketplace (Xingtu) spread metrics endpoint for a specified KOL ID and summarize audience, content performance, and commercial indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a URL query parameter and could be exposed through copied URLs, shell history, proxy logs, or request logging. <br>
Mitigation: Use a limited, rotatable JUST_ONE_API_TOKEN and avoid logging full request URLs or sharing command invocations that include token values. <br>
Risk: The skill sends KOL IDs and selected filters to JustOneAPI's hosted API. <br>
Mitigation: Install only when you trust JustOneAPI and the requested Douyin/Xingtu lookup data is appropriate to send to that service. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-get-kol-spread-info) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_spread_info&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_spread_info&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; calls getKolSpreadInfoV1 with kolId and optional query parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
