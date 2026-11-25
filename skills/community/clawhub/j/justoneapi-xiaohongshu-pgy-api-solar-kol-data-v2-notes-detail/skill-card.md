## Description:

Call GET /api/xiaohongshu-pgy/api/solar/kol/dataV2/notesDetail/v1 for Xiaohongshu Creator Marketplace (Pugongying) User Published Notes through JustOneAPI with userId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI's Xiaohongshu Creator Marketplace (Pugongying) Published Notes endpoint for a KOL user ID, then summarize note metadata and engagement signals for creator monitoring and campaign research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends userId values and a JustOneAPI token to api.justoneapi.com.

Mitigation: Install only when that data sharing is acceptable for the intended workflow.

Risk: The JustOneAPI token is sent as a request URL query parameter, which can be exposed through transcripts, command lines, logs, or request URLs.

Mitigation: Use a narrowly scoped, revocable token; avoid sharing logs or transcripts that include command lines or URLs; rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v2_notes_detail&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v2_notes_detail&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-api-solar-kol-data-v2-notes-detail)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with optional shell command and JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; sends userId and optional query filters to the JustOneAPI endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
