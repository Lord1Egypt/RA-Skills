## Description:

Call GET /api/weibo/get-post-comments/v1 for Weibo Post Comments through JustOneAPI with mid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to call JustOneAPI's Weibo post comments endpoint for a supplied post mid and retrieve comment text, authors, timestamps, and pagination-aware results for feedback analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token can be exposed through process arguments or URL query strings.

Mitigation: Use a narrowly scoped, revocable token; avoid logging full command lines or request URLs; prefer a safer secret channel and authorization header if the provider supports it.

Risk: The skill sends user-provided Weibo post identifiers and pagination or sorting parameters to a third-party API service.

Mitigation: Confirm the request scope with the user, avoid submitting sensitive identifiers unnecessarily, and review returned content before relying on it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-weibo-get-post-comments)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_post_comments&utm_content=project_link)
- [Generated Operation Reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls one GET endpoint, requires JUST_ONE_API_TOKEN, and returns parsed JSON from the JustOneAPI backend.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
