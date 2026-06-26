## Description: <br>
Call GET /api/xiaohongshu-pgy/api/solar/kol/dataV2/kolFeatureTags/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Feature Tags through JustOneAPI with userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a JustOneAPI endpoint that retrieves Xiaohongshu Creator Marketplace creator feature tags by userId for segmentation, discovery, and creator classification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token may be exposed through command-line arguments or request URLs. <br>
Mitigation: Use a scoped or short-lived JustOneAPI token, avoid environments that log command lines or full request URLs, and rotate the token if exposure is suspected. <br>
Risk: Backend error payloads may include request context or operational details. <br>
Mitigation: Review error output before sharing it and avoid pasting token values, full request URLs, or sensitive identifiers into chat messages or logs. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-api-solar-kol-data-v2-kol-feature-tags) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v2_kol_feature_tags&utm_content=project_link) <br>
- [Generated operation reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; the endpoint requires userId and returns raw JSON after a short endpoint-specific summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
