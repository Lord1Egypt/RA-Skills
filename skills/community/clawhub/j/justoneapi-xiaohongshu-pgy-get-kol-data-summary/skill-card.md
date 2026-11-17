## Description:

Call GET /api/xiaohongshu-pgy/get-kol-data-summary/v2 for Xiaohongshu Creator Marketplace (Pugongying) Data Summary through JustOneAPI with business and kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI's Xiaohongshu Creator Marketplace endpoint for creator activity, engagement, and audience growth summaries. It supports creator evaluation, campaign planning, and benchmarking for a specified KOL ID and business type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token, KOL ID, and business parameter are sent to api.justoneapi.com.

Mitigation: Use the skill only when sending those values to JustOneAPI is acceptable for the intended workflow.

Risk: The API token can be exposed through command arguments, shell history, process telemetry, proxy logs, or URL logs.

Mitigation: Prefer short-lived or narrowly scoped tokens, avoid pasting tokens into chats or logs, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-get-kol-data-summary)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_data_summary&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_data_summary&utm_content=project_link)
- [Generated Operations Reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Markdown, JSON]

**Output Format:** [Markdown summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN, kolId, and business; includes the operation ID and endpoint path used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
