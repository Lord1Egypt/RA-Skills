## Description: <br>
Call GET /api/xiaohongshu-pgy/api/solar/kol/dataV3/dataSummary/v1 for Xiaohongshu Creator Marketplace (Pugongying) Data Summary through JustOneAPI with userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to call the JustOneAPI Xiaohongshu Creator Marketplace data summary endpoint for creator evaluation, campaign planning, and creator benchmarking. It requires a JustOneAPI token and a creator userId, with optional business type selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The marketplace token is passed as a URL query parameter and may be exposed through logs, browser history, screenshots, or support bundles. <br>
Mitigation: Use a scoped and revocable token when available, avoid sharing generated URLs or logs, and rotate the token if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-api-solar-kol-data-v3-data-summary) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v3_data_summary&utm_content=project_link) <br>
- [Generated operation reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with an inline shell command and JSON API response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill targets one GET endpoint, uses userId as the required lookup parameter, and summarizes endpoint-specific results before returning raw JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
