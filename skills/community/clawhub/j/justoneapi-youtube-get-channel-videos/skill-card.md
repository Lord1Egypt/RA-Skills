## Description:

Call GET /api/youtube/get-channel-videos/v1 for YouTube Channel Videos through JustOneAPI with channelId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call JustOneAPI's YouTube channel videos endpoint for a supplied channelId and review a short summary followed by the raw JSON response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles the JustOneAPI token in ways that can expose it through command arguments and URL query strings.

Mitigation: Use a narrowly scoped token where possible, avoid environments that log command arguments or full URLs, and rotate the token if it may have appeared in logs.

Risk: The security verdict is suspicious even though no malicious behavior was found.

Mitigation: Review the skill before installing and confirm the credential handling is acceptable for the intended environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-youtube-get-channel-videos)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youtube_get_channel_videos&utm_content=project_link)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youtube_get_channel_videos&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON, with shell command examples for endpoint execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; accepts channelId and optional cursor.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
