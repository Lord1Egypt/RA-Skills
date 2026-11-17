## Description:

Analyze Reddit workflows with JustOneAPI, including post Details, post Comments, and keyword Search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Reddit post details, post comments, and keyword search results through JustOneAPI. It is useful when the user can provide a Reddit post ID, cursor, pagination token, or keyword and wants an API-backed answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command-line arguments, URL query parameters, logs, or process metadata.

Mitigation: Use a narrowly scoped token when available, avoid logging commands or full request URLs, and rotate the token if it may have appeared in logs or process captures.

Risk: Tokens with billing, quota, or broad JustOneAPI access can increase impact if leaked.

Mitigation: Review token scope before installation and prefer a token limited to the minimum access needed for Reddit requests.

Risk: Sensitive Reddit search terms or identifiers may be sent to JustOneAPI during normal operation.

Mitigation: Avoid sensitive search terms where possible and minimize shared parameters to the post IDs, cursors, pagination tokens, or keywords required for the task.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-reddit)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_reddit&utm_content=project_link)
- [Reddit Operations](generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown answer with selected API-backed JSON details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and task-specific Reddit identifiers or keywords; the helper issues GET requests to JustOneAPI.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
