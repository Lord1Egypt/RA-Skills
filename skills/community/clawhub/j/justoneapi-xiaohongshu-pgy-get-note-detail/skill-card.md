## Description:

Call GET /api/xiaohongshu-pgy/get-note-detail/v1 for Xiaohongshu Creator Marketplace (Pugongying) Note Details through JustOneAPI with noteId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve Xiaohongshu Creator Marketplace (Pugongying) note details by noteId through JustOneAPI for content analysis, archiving, and campaign review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is sent as a URL query parameter, which can expose credentials in logs or telemetry.

Mitigation: Use a scoped, revocable token; avoid placing token values in chat, screenshots, or logs; and review runtime logs before using long-lived or high-privilege credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-get-note-detail)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_note_detail&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_note_detail&utm_content=project_link)
- [Generated operation reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON]

**Output Format:** [Markdown summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and noteId; optional acceptCache controls cache use.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
