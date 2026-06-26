## Description: <br>
Call GET /api/douyin-xingtu/gw/api/data_sp/get_author_convert_ability/v1 for Douyin Creator Marketplace (Xingtu) Conversion Analysis through JustOneAPI with oAuthorId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to call JustOneAPI for Douyin Creator Marketplace (Xingtu) creator conversion analysis. It supports creator evaluation, campaign planning, and marketplace research using an author ID plus optional platform and time-range filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is passed as a query parameter and may appear in URLs, logs, screenshots, or browser history. <br>
Mitigation: Use a narrowly scoped, revocable token when available, avoid sharing logs or copied URLs, and rotate the token if exposure is possible. <br>
Risk: The skill returns creator marketplace analytics that may be incomplete, stale, or affected by backend API errors. <br>
Mitigation: Review the endpoint-specific summary and raw backend payload before using results for campaign planning or creator evaluation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-data-sp-get-author-convert-ability) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_convert_ability&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_convert_ability&utm_content=project_link) <br>
- [Generated operation reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and the oAuthorId query parameter; optional filters include platform and range.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
