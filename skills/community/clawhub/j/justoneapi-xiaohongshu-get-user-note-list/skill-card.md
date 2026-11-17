## Description:

Calls the JustOneAPI Xiaohongshu get-user-note-list v2 or v4 endpoint to retrieve a user's published RedNote notes by userId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to retrieve and summarize Xiaohongshu (RedNote) published-note metadata, covers, publish times, and pagination state for account monitoring through JustOneAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token may be exposed through command-line process listings or URL/query logging.

Mitigation: Use short-lived, scoped JustOneAPI tokens when available, avoid broad permissions, rotate tokens after use, and keep token values out of chat messages, screenshots, and logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-get-user-note-list)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_user_note_list&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_user_note_list&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes the endpoint response before returning raw JSON and includes backend error payloads when calls fail.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
