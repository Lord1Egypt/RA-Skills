## Description:

Call GET /api/xiaohongshu-pgy/api/solar/cooperator/user/blogger/userId/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Profile through JustOneAPI with userId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to retrieve Xiaohongshu Creator Marketplace creator profile data for influencer vetting, benchmark analysis, and campaign planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through request URLs, command arguments, logs, screenshots, or process telemetry.

Mitigation: Use a narrowly scoped, revocable token; avoid sharing command logs or process telemetry; and rotate the token if exposure is suspected.

Risk: The skill depends on an external JustOneAPI endpoint and may return backend errors or unavailable responses.

Mitigation: Check the operation ID, required userId parameter, and returned backend payload before relying on results.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-api-solar-cooperator-user-blogger-user-id)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_cooperator_user_blogger_user_id&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_cooperator_user_blogger_user_id&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown summary followed by raw JSON when the API call succeeds; JSON error payloads when the backend fails.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a userId query parameter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
