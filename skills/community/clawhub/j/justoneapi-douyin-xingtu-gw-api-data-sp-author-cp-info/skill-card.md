## Description: <br>
Call GET /api/douyin-xingtu/gw/api/data_sp/author_cp_info/v1 for Douyin Creator Marketplace (Xingtu) Cost Performance Analysis through JustOneAPI with oAuthorId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to query JustOneAPI for Douyin Creator Marketplace (Xingtu) cost performance data by creator ID. It supports creator evaluation, campaign planning, and marketplace research with pricing, exposure, and engagement efficiency indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token and queried creator IDs can be exposed through chat, screenshots, logs, command history, process listings, proxy logs, or API logs because the helper passes the token through the command line and URL query string. <br>
Mitigation: Keep JUST_ONE_API_TOKEN out of chat, screenshots, and logs; install only if you trust JustOneAPI with the token and queried creator IDs; rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-data-sp-author-cp-info) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_cp_info&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_cp_info&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and an oAuthorId query parameter; platform defaults to SHORT_VIDEO when omitted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
