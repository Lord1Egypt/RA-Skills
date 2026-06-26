## Description: <br>
Call GET /api/douyin-xingtu/gw/api/data_sp/item_report_detail/v1 for Douyin Creator Marketplace (Xingtu) Item Report Details through JustOneAPI with itemId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Douyin Creator Marketplace (Xingtu) item report details through JustOneAPI for a specific itemId. It supports item performance analysis by returning key metrics and report fields from the documented endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token is sent in the request URL and may be exposed through URL logs, copied command output, chat messages, screenshots, or similar channels. <br>
Mitigation: Use a scoped, revocable JustOneAPI token; avoid logging full request URLs or sharing outputs that may contain request details; rotate the token if URL logs may have captured it. <br>
Risk: The skill makes authenticated requests to a third-party API provider. <br>
Mitigation: Install and run it only when the JustOneAPI publisher and endpoint are trusted for the intended workflow. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_item_report_detail&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_item_report_detail&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-data-sp-item-report-detail) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON when results are available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a scoped JUST_ONE_API_TOKEN and an itemId query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
