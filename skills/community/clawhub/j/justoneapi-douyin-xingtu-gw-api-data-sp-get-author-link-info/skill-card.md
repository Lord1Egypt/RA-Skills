## Description: <br>
Call GET /api/douyin-xingtu/gw/api/data_sp/get_author_link_info/v1 for Douyin Creator Marketplace (Xingtu) Creator Link Metrics through JustOneAPI with oAuthorId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a JustOneAPI endpoint for Douyin Creator Marketplace (Xingtu) creator link metrics. It supports creator evaluation, campaign planning, and marketplace research using an author ID plus optional platform and industry filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token is sent as a URL query parameter to api.justoneapi.com, which can expose the credential through request logs, copied URLs, or chat transcripts. <br>
Mitigation: Pass the token from JUST_ONE_API_TOKEN, avoid logging full request URLs or token values, and prefer a short-lived or easily revocable token when available. <br>
Risk: The skill sends requests to a third-party JustOneAPI service using sensitive credentials. <br>
Mitigation: Install and run it only when the JustOneAPI publisher and endpoint are trusted for the intended workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-data-sp-get-author-link-info) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_link_info&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_link_info&utm_content=project_link) <br>
- [Generated operations reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a required JUST_ONE_API_TOKEN credential and required oAuthorId query parameter; optional platform and industryTag filters are supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
