## Description:

Call GET /api/weibo/get-user-video-list/v1 for Weibo User Video List through JustOneAPI with uid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to call JustOneAPI's Weibo user video-list endpoint for a supplied uid and optional pagination cursor, then summarize results and return raw JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command-line arguments and systems that log full request URLs.

Mitigation: Use a short-lived, narrowly scoped token, avoid shared machines, avoid logging full URLs or command lines, and rotate the token if it may have appeared in command history, process telemetry, or URL logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-weibo-get-user-video-list)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_user_video_list&utm_content=project_link)
- [Weibo User Video List operations](generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON from the API helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; endpoint input requires uid and supports optional cursor pagination.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
