## Description: <br>
Call GET /api/xiaohongshu-pgy/api/solar/kol/dataV2/costEffective/v1 for Xiaohongshu Creator Marketplace (Pugongying) Cost Effectiveness Analysis through JustOneAPI with userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a focused JustOneAPI endpoint for Xiaohongshu Creator Marketplace cost effectiveness data. It supports campaign evaluation workflows by retrieving pricing, reach, and engagement efficiency indicators for a supplied KOL userId. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a JustOneAPI token and queried Xiaohongshu userId to the JustOneAPI endpoint. <br>
Mitigation: Use a scoped or revocable token where possible, avoid shared shells or logging-heavy environments, and do not paste token values into chat, logs, screenshots, or client-side code. <br>
Risk: Campaign evaluation can be affected by missing, stale, or backend-specific API data. <br>
Mitigation: Review the returned backend payload and operation ID before making business decisions from the summarized results. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v2_cost_effective&utm_content=project_link) <br>
- [Just One API dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v2_cost_effective&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-api-solar-kol-data-v2-cost-effective) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/justoneapi) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and a Xiaohongshu KOL userId; successful calls return the backend JSON response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
