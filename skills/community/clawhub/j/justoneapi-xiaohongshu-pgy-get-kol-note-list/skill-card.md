## Description:

Call GET /api/xiaohongshu-pgy/get-kol-note-list/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Note List through JustOneAPI with adSwitch, kolId, and orderType.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to call JustOneAPI's Xiaohongshu Pugongying creator note list endpoint for a specified KOL, ad traffic filter, and sort order, then summarize content metadata, publish time, and engagement indicators for content analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required JustOneAPI token is handled in a URL query string, creating a credential-exposure risk.

Mitigation: Use a narrowly scoped token where possible, avoid logging command lines or full request URLs, rotate the token after suspected exposure, and prefer Authorization-header authentication if the provider offers it.

Risk: Broad, paid, or long-lived JustOneAPI tokens increase the impact of accidental exposure.

Mitigation: Review token authority before installing or running the skill and avoid using credentials with unnecessary scope or duration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-get-kol-note-list)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_note_list&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_note_list&utm_content=project_link)
- [Generated Operation Documentation](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; expected use includes a short endpoint-specific summary followed by raw JSON.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
