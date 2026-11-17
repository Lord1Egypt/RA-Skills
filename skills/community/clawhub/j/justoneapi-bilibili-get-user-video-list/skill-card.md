## Description:

Call GET /api/bilibili/get-user-video-list/v2 for Bilibili User Published Videos through JustOneAPI with uid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to fetch Bilibili user published video lists by UID through JustOneAPI, supporting creator monitoring and content performance analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a JustOneAPI token to api.justoneapi.com for Bilibili lookup requests.

Mitigation: Use a scoped, revocable token where possible and install only when that token use is acceptable.

Risk: Tokens or request details may appear in command-line telemetry, logs, screenshots, or process traces.

Mitigation: Avoid sharing run logs or process traces, do not paste token values into chat, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/justoneapi/skills/justoneapi-bilibili-get-user-video-list)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_video_list&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_video_list&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Markdown summary with optional raw JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a Bilibili UID; supports an optional pagination parameter.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
