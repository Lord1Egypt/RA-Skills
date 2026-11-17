## Description:

Analyze YouTube workflows with JustOneAPI, including video Details and channel Videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve YouTube video details or channel video lists through JustOneAPI when they can provide required identifiers such as videoId or channelId.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command-line arguments and URL query logs.

Mitigation: Use a narrowly scoped token, avoid recording command lines or request URLs in shared logs, and rotate the token if it may have been captured in shell history, traces, or monitoring systems.

Risk: Authenticated YouTube lookups depend on user-supplied identifiers and can return data outside the intended scope if identifiers are wrong.

Mitigation: Ask for missing required parameters, do not invent videoId or channelId values, and echo the selected identifiers in the response so the request scope is explicit.

## Reference(s):

- [YouTube operations](generated/operations.md)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youtube&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youtube&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-youtube)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain-language Markdown response with selected YouTube fields and optional formatted JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should include the selected operation ID, user-provided scope such as videoId or channelId, and backend error payloads when a request fails.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
