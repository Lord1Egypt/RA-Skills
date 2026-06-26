## Description: <br>
Call GET /api/douyin-xingtu/gw/api/data_sp/author_link_struct/v1 for Douyin Creator Marketplace (Xingtu) Creator Link Structure through JustOneAPI with oAuthorId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to call JustOneAPI's Douyin Creator Marketplace (Xingtu) creator Link Structure endpoint for creator performance analysis by author ID and optional platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI access token is sent as a query parameter and may be exposed through copied URLs, logs, screenshots, or failed request details. <br>
Mitigation: Use a limited or revocable token, avoid sharing logs or request URLs, and rotate the token if exposure is suspected. <br>
Risk: Endpoint data and backend error payloads may include sensitive account or creator-performance information. <br>
Mitigation: Share only the minimum necessary response details and avoid posting raw backend payloads in public or untrusted channels. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-data-sp-author-link-struct) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_link_struct&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_link_struct&utm_content=project_link) <br>
- [Generated Operations Reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with raw JSON response and inline shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN; oAuthorId is required and platform defaults to SHORT_VIDEO.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
