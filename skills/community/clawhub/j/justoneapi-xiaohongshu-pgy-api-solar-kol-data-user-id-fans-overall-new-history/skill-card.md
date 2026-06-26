## Description: <br>
Call GET /api/xiaohongshu-pgy/api/solar/kol/data/userId/fans_overall_new_history/v1 for Xiaohongshu Creator Marketplace (Pugongying) Follower Growth History through JustOneAPI with userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query JustOneAPI for Xiaohongshu Creator Marketplace (Pugongying) creator follower growth history by userId. It supports trend tracking, audience analysis, and creator performance monitoring from the returned historical points, trend signals, and growth metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API call sends creator userIds and a JustOneAPI token to api.justoneapi.com. <br>
Mitigation: Install only when that data sharing is acceptable for the use case, and prefer scoped or short-lived tokens when available. <br>
Risk: The token is supplied on the command line and is used as a query parameter. <br>
Mitigation: Avoid logging full commands, shell history, request URLs, or backend payloads that may expose the token; consider a future version that reads tokens from a safer secret source. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_user_id_fans_overall_new_history&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_user_id_fans_overall_new_history&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-api-solar-kol-data-user-id-fans-overall-new-history) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and a Xiaohongshu Creator Marketplace userId; optional query parameters select date range and growth metric.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
