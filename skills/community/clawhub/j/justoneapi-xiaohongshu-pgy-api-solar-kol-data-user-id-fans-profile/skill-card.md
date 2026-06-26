## Description: <br>
Call GET /api/xiaohongshu-pgy/api/solar/kol/data/userId/fans_profile/v1 for Xiaohongshu Creator Marketplace (Pugongying) Follower Distribution through JustOneAPI with userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a JustOneAPI endpoint for Xiaohongshu Creator Marketplace follower distribution data by userId, supporting creator evaluation, campaign planning, and benchmarking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required JustOneAPI token can be exposed through command-line arguments or query-string authentication. <br>
Mitigation: Use a protected environment variable or secret store, avoid shared or logging-heavy machines, and prefer header-based authentication if the upstream API supports it. <br>
Risk: API responses may contain audience demographics, interests, and campaign-planning data for a creator lookup. <br>
Mitigation: Handle returned JSON according to the user's privacy and commercial-data policies, and avoid storing or logging unnecessary response data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-api-solar-kol-data-user-id-fans-profile) <br>
- [JustOneAPI API homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_user_id_fans_profile&utm_content=project_link) <br>
- [Generated operation reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and userId; returns raw JSON after a short endpoint-specific summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
