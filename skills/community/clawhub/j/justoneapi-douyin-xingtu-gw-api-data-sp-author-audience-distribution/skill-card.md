## Description: <br>
Call GET /api/douyin-xingtu/gw/api/data_sp/author_audience_distribution/v1 for Douyin Creator Marketplace (Xingtu) Audience Distribution through JustOneAPI with oAuthorId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a JustOneAPI endpoint for Douyin Creator Marketplace audience distribution data by creator author ID, supporting creator evaluation, campaign planning, and marketplace research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper sends JUST_ONE_API_TOKEN as a URL query parameter to api.justoneapi.com, which can expose the token through copied URLs, command histories, logs, screenshots, or error traces. <br>
Mitigation: Use an environment variable for the token, share only redacted commands and logs, and confirm trust in JustOneAPI before installing or running the skill. <br>
Risk: The endpoint queries creator audience information for a supplied oAuthorId. <br>
Mitigation: Confirm the creator ID and filters are intended for the task, and avoid exposing user-provided IDs or returned audience data beyond the agent workflow that needs them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-data-sp-author-audience-distribution) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_audience_distribution&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_audience_distribution&utm_content=project_link) <br>
- [Generated Operations Reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and endpoint JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, JUST_ONE_API_TOKEN, and an oAuthorId query parameter; optional platform and linkType filters are supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
