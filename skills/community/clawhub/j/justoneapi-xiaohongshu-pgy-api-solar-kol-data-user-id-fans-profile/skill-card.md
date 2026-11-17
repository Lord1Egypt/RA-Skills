## Description:

Call GET /api/xiaohongshu-pgy/api/solar/kol/data/userId/fans_profile/v1 for Xiaohongshu Creator Marketplace (Pugongying) Follower Distribution through JustOneAPI with userId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to call a focused JustOneAPI Xiaohongshu Creator Marketplace endpoint for follower distribution data by KOL user ID. The returned data supports creator evaluation, campaign planning, and creator benchmarking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a JustOneAPI token for the follower-distribution endpoint, and command-line or URL handling can expose credentials in local process or logging surfaces.

Mitigation: Use a short-lived or limited-scope token where available, avoid shared machines and process logging, do not paste token values into chat or screenshots, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-api-solar-kol-data-user-id-fans-profile)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_user_id_fans_profile&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_user_id_fans_profile&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with a shell command example and JSON API response handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN; the API helper emits parsed JSON on successful backend responses.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
