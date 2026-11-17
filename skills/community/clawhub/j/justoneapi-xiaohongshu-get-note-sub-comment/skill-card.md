## Description:

Call GET /api/xiaohongshu/get-note-sub-comment/v2 for Xiaohongshu (RedNote) Comment Replies through JustOneAPI with commentId and noteId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Xiaohongshu (RedNote) comment-reply data through JustOneAPI for thread analysis and feedback research. The skill requires noteId and commentId, supports an optional pagination cursor, and returns a short endpoint-specific summary followed by raw JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reusable JustOneAPI token is sent as a URL query parameter and may appear in service, proxy, or intermediary request logs.

Mitigation: Use a narrowly scoped token where available, avoid sharing tokens in chat or logs, and review installation carefully when the token has paid quota or access to sensitive data.

Risk: The skill can retrieve social platform comment-reply data tied to note and comment identifiers.

Mitigation: Use only identifiers the user is authorized to inspect and summarize returned content with care when it may include personal or sensitive information.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_note_sub_comment&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_note_sub_comment&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-get-note-sub-comment)
- [Generated operation reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON]

**Output Format:** [Markdown summary with shell command examples and raw JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; noteId and commentId are required query inputs, with lastCursor optional for pagination.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
