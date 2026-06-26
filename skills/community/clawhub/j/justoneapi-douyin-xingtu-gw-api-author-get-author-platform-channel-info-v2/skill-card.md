## Description: <br>
Call GET /api/douyin-xingtu/gw/api/author/get_author_platform_channel_info_v2/v1 for Douyin Creator Marketplace (Xingtu) Creator Channel Metrics through JustOneAPI with oAuthorId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to call a focused JustOneAPI endpoint for Douyin Creator Marketplace (Xingtu) creator channel metrics, using an author ID and optional platform filter to retrieve distribution and channel performance data for creator evaluation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token is sent as a URL query parameter, which can expose credentials in copied request URLs, logs, traces, screenshots, or error reports. <br>
Mitigation: Use a low-privilege token that can be rotated, pass it through JUST_ONE_API_TOKEN, and avoid sharing command output, logs, screenshots, traces, or error reports that could include full request URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-gw-api-author-get-author-platform-channel-info-v2) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_author_get_author_platform_channel_info_v2&utm_content=project_link) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_author_get_author_platform_channel_info_v2&utm_content=project_link) <br>
- [Generated operation reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; the endpoint requires oAuthorId and accepts an optional platform query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
