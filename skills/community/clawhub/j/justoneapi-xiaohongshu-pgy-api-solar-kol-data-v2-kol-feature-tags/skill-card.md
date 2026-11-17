## Description:

Call GET /api/xiaohongshu-pgy/api/solar/kol/dataV2/kolFeatureTags/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Feature Tags through JustOneAPI with userId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve Xiaohongshu Creator Marketplace creator feature tags for a known userId. It supports creator segmentation, discovery, and classification workflows through the JustOneAPI endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token is passed through command-line arguments and URL query parameters, which can expose credentials in logs, shell history, process metadata, or full URL captures.

Mitigation: Use a narrowly scoped, revocable JustOneAPI token, avoid environments that log process arguments or full URLs, and do not paste token values into chat, screenshots, or logs.

Risk: Creator lookup requests may involve third-party platform data and creator identifiers.

Mitigation: Query only creator IDs the user is authorized to access and review backend responses before relying on them in segmentation or discovery workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-api-solar-kol-data-v2-kol-feature-tags)
- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v2_kol_feature_tags&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v2_kol_feature_tags&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell command examples; endpoint runner returns formatted JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a userId query parameter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
