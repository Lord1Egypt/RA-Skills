## Description: <br>
Call GET /api/douyin-xingtu/gw/api/data_sp/get_author_convert_videos_or_products/v1 for Douyin Creator Marketplace (Xingtu) Conversion Resources through JustOneAPI with oAuthorId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to call a focused JustOneAPI endpoint for Douyin Creator Marketplace conversion resources by creator ID. It supports commerce analysis and campaign optimization by returning conversion-related products or videos from the API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a query parameter and can be exposed through full URL logging, shell history, screenshots, or shared error output. <br>
Mitigation: Avoid logging or sharing full request URLs, pass the token through JUST_ONE_API_TOKEN, use the least-privileged token available, and rotate it if exposure is suspected. <br>
Risk: The skill sends requests and credentials to the third-party api.justoneapi.com service. <br>
Mitigation: Install and use it only when the publisher and service are trusted for the intended data and credential handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-data-sp-get-author-convert-videos-or-products) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_convert_videos_or_products&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_convert_videos_or_products&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; required endpoint input is oAuthorId, with optional query filters for platform, industryId, range, detailType, and page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
