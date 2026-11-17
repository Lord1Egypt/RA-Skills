## Description:

Call 2 get-note-comment versions for Xiaohongshu (RedNote) Note Comments through JustOneAPI with noteId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to fetch Xiaohongshu (RedNote) note comments by noteId through JustOneAPI for feedback analysis, sentiment analysis, and community monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command arguments, full request URLs, or environment logging.

Mitigation: Use a narrowly scoped or disposable token when available, avoid environments that log process arguments or URLs, and never paste token values into chat messages, screenshots, or logs.

Risk: Returned Xiaohongshu comment and author data may include personal information.

Mitigation: Limit retention and sharing of returned data, and handle it according to the user's privacy, compliance, and data-use requirements.

## Reference(s):

- [JustOneAPI API homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_note_comment&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_note_comment&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-get-note-comment)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and noteId; returned data may include Xiaohongshu comments, author profile data, timestamps, and interaction data.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
