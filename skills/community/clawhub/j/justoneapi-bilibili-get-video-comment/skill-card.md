## Description:

Call GET /api/bilibili/get-video-comment/v2 for Bilibili Video Comments through JustOneAPI with aid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch Bilibili video comments by archive ID through JustOneAPI, then summarize commenter profiles, comment text, likes, and sentiment or moderation signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JustOneAPI tokens can appear in process listings, command lines, full request URLs, or logs.

Mitigation: Use narrowly scoped or short-lived tokens when available, avoid sharing logs that include commands or request URLs, and rotate any token that may have been exposed.

Risk: Bilibili video identifiers and returned comment or profile data are sent through JustOneAPI.

Mitigation: Install and use the skill only when that data flow is acceptable for the intended workflow and audience.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-bilibili-get-video-comment)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_comment&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_comment&utm_content=project_link)
- [Bilibili Video Comments operations](generated/operations.md)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Markdown, JSON, Guidance]

**Output Format:** [Markdown summary with endpoint details and raw JSON output when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and Bilibili aid; optional cursor supports pagination.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
