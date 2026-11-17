## Description:

Call 3 get-note-detail versions for Xiaohongshu (RedNote) Note Details through JustOneAPI with noteId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve Xiaohongshu (RedNote) note detail data by noteId through JustOneAPI. The returned media and engagement data can support content analysis, archiving, and campaign research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through query URLs or process arguments.

Mitigation: Use a narrowly scoped token, avoid environments that log command lines or full request URLs, and rotate the token if it may have appeared in telemetry, proxy logs, or API gateway logs.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-get-note-detail)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_note_detail&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_note_detail&utm_content=project_link)
- [Generated Operations Reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON from the selected JustOneAPI endpoint]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and noteId; backend errors include the backend payload and operation ID.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
