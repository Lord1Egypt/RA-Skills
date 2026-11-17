## Description:

Call GET /api/xiaohongshu-pgy/api/solar/kol/get_similar_kol/v1 for Xiaohongshu Creator Marketplace (Pugongying) Similar Creators through JustOneAPI with userId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to call JustOneAPI's Xiaohongshu Creator Marketplace similar-creators endpoint with a KOL userId, then summarize audience and creator-discovery signals for benchmarking and shortlist building.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is passed through command-line arguments and URL query parameters, which can expose it in logs or process metadata.

Mitigation: Use a narrowly scoped token when available, avoid exposing command lines or logs, and rotate the token if it may have appeared in process telemetry or request logs.

Risk: The token may carry account, billing, or quota privileges.

Mitigation: Review the token's privileges before installation or execution and avoid using broadly privileged credentials for routine calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-api-solar-kol-get-similar-kol)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_get_similar_kol&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_get_similar_kol&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown summary followed by raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a required JustOneAPI token and userId; backend errors include the backend payload and operation ID.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
