## Description:

Call GET /api/xiaohongshu-pgy/api/solar/kol/data/userId/fans_overall_new_history/v1 for Xiaohongshu Creator Marketplace (Pugongying) Follower Growth History through JustOneAPI with userId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call a JustOneAPI endpoint for Xiaohongshu Creator Marketplace follower growth history by userId, then summarize historical points, trend signals, and growth metrics for creator monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token is passed through command-line arguments and URL query parameters where it may appear in process listings, command history, proxy logs, or API logs.

Mitigation: Use a narrowly scoped, revocable token, avoid pasting token values into chat or logs, and rotate the token if exposure is suspected.

Risk: Requests send the token and Xiaohongshu user IDs to JustOneAPI.

Mitigation: Install and use the skill only when JustOneAPI is trusted for the intended data and account context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-api-solar-kol-data-user-id-fans-overall-new-history)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_user_id_fans_overall_new_history&utm_content=project_link)
- [Generated Operation Reference](generated/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a required JustOneAPI token, a required userId, and optional dateType and increaseType query parameters.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
