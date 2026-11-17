## Description:

Call GET /api/xiaohongshu-pgy/get-kol-note-rate/v1 for Xiaohongshu Creator Marketplace (Pugongying) Note Performance Metrics through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Xiaohongshu Creator Marketplace note performance metrics for a specific KOL through JustOneAPI. It supports content efficiency analysis, creator benchmarking, and campaign planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A JustOneAPI token and the requested kolId are sent to api.justoneapi.com.

Mitigation: Use a narrowly scoped, revocable token and avoid exposing token values in chat, screenshots, logs, shell history, proxy logs, or process monitors.

Risk: If token exposure is suspected, the credential could be reused until revoked.

Mitigation: Rotate the JustOneAPI token promptly after suspected exposure.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_note_rate&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_note_rate&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, JSON]

**Output Format:** [Markdown summary with endpoint details and raw JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a kolId query parameter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
