## Description: <br>
Call GET /api/douyin-xingtu/get-kol-convert-videos-or-products/v1 for Douyin Creator Marketplace (Xingtu) Conversion Resources through JustOneAPI with detailType, kolId, and page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a JustOneAPI Douyin Creator Marketplace (Xingtu) endpoint for conversion resources by KOL ID, resource type, and page. It supports commerce analysis and campaign optimization workflows that need video or product conversion data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a URL query parameter and could be exposed through command histories, logs, telemetry, or shared request URLs. <br>
Mitigation: Use a limited-scope or easily rotated token when available, avoid pasting token values into chat or logs, avoid sharing full request URLs, and rotate the token if exposure is suspected. <br>
Risk: The skill depends on a live external JustOneAPI endpoint and valid user-supplied parameters for KOL ID, detail type, and page. <br>
Mitigation: Ask for missing required parameters before execution, keep user-provided IDs and filters unchanged, and include backend error payloads with the operation ID when requests fail. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-get-kol-convert-videos-or-products) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_convert_videos_or_products&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_convert_videos_or_products&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a short endpoint-specific summary before raw JSON when used as documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
