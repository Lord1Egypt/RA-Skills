## Description: <br>
Call GET /api/tiktok/get-user-detail/v1 for TikTok User Profile through JustOneAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve TikTok profile details through JustOneAPI when given a TikTok uniqueId or secUid. It supports profile lookup, audience analysis, account tracking, and verified-status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token could be exposed in chat messages, logs, screenshots, or shell history. <br>
Mitigation: Pass the token through the JUST_ONE_API_TOKEN environment variable, avoid pasting token values into shared surfaces, and rotate the token if exposure is suspected. <br>
Risk: TikTok profile lookup results can contain personal data and may be misused for harassment or covert profiling. <br>
Mitigation: Use the skill only for legitimate profile lookup and analysis, minimize retention and sharing of returned data, and follow applicable privacy and acceptable-use requirements. <br>
Risk: Requests send TikTok identifiers and the JustOneAPI token to api.justoneapi.com. <br>
Mitigation: Install and run the skill only when the user trusts JustOneAPI and is comfortable sending lookup requests to that service. <br>


## Reference(s): <br>
- [JustOneAPI API homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_user_detail&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JUST_ONE_API_TOKEN for authentication and may include raw backend JSON after a short endpoint-specific summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
