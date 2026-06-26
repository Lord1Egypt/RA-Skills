## Description: <br>
Call GET /api/xiaohongshu-pgy/api/solar/kol/dataV2/kolContentTags/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Content Tags through JustOneAPI with userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to call JustOneAPI's Xiaohongshu Creator Marketplace endpoint for a creator's content tags by userId, supporting creator evaluation, campaign planning, and benchmarking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marked this release suspicious because API token handling could expose the token. <br>
Mitigation: Install only if you trust JustOneAPI, use a limited-scope or disposable token, avoid shared or heavily logged systems, and rotate the token if it may have appeared in logs or process listings. <br>
Risk: The helper passes authentication through request parameters for the JustOneAPI call. <br>
Mitigation: Prefer a revised helper that reads the token from a protected environment variable and uses header-based authentication if the provider supports it. <br>


## Reference(s): <br>
- [Endpoint operations reference](generated/operations.md) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v2_kol_content_tags&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v2_kol_content_tags&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-api-solar-kol-data-v2-kol-content-tags) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Endpoint-specific Markdown summary followed by raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and userId.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
