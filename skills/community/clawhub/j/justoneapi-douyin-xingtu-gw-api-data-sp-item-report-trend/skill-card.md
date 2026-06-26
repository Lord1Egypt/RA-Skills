## Description: <br>
Call GET /api/douyin-xingtu/gw/api/data_sp/item_report_trend/v1 for Douyin Creator Marketplace (Xingtu) Item Report Trends through JustOneAPI with itemId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to request Douyin Creator Marketplace (Xingtu) item report trend data through JustOneAPI for creator evaluation, campaign planning, and marketplace research. It requires an itemId and a JustOneAPI token before calling the endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is passed as a query parameter, which can expose credentials if full request URLs are logged or shared. <br>
Mitigation: Use a limited or disposable token when available, avoid logging full request URLs, and do not paste token values into chat, screenshots, or shared command output. <br>
Risk: The skill returns Douyin/Xingtu reporting data through a third-party API provider. <br>
Mitigation: Install only if you trust JustOneAPI with the requested Douyin/Xingtu data and token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-data-sp-item-report-trend) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_item_report_trend&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_item_report_trend&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with optional raw JSON response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses operation gwApiDataSpItemReportTrendV1 and requires itemId plus JUST_ONE_API_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
