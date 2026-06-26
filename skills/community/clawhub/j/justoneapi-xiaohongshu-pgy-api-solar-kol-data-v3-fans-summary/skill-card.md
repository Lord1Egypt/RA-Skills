## Description: <br>
Call GET /api/xiaohongshu-pgy/api/solar/kol/dataV3/fansSummary/v1 for Xiaohongshu Creator Marketplace (Pugongying) Follower Summary through JustOneAPI with userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query JustOneAPI for Xiaohongshu Creator Marketplace follower summary data by userId. It supports audience analysis and creator benchmarking by returning endpoint-specific metrics with raw JSON for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token to query a third-party follower-summary API. <br>
Mitigation: Use a limited or short-lived token if available, keep token values out of chat messages, logs, screenshots, and URLs, and rotate the token if it may have been exposed. <br>
Risk: API errors or unexpected response payloads can affect the reliability of generated summaries. <br>
Mitigation: Include the returned error payload and operation ID when a request fails, and review raw JSON before relying on follower metrics. <br>


## Reference(s): <br>
- [JustOneAPI API homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v3_fans_summary&utm_content=project_link) <br>
- [Xiaohongshu follower summary operations](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with raw JSON response data and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and a userId query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
