## Description: <br>
Call GET /api/kuaishou/get-video-comment/v1 for Kuaishou Video Comments through JustOneAPI with videoId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch public comments for a specific Kuaishou video through JustOneAPI, then summarize engagement signals such as comment content, author information, likes, and replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a URL query parameter and may appear in command output, request URLs, or logs. <br>
Mitigation: Use a scoped or disposable token where possible, avoid sharing logs or screenshots that may include request URLs, and rotate the token if exposure is suspected. <br>
Risk: The skill retrieves comments for caller-provided Kuaishou video IDs through a third-party API provider. <br>
Mitigation: Install and run it only when you trust JustOneAPI with the token and queried video IDs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-kuaishou-get-video-comment) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_video_comment&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_video_comment&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with raw JSON response when requested or after the endpoint-specific summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and a Kuaishou videoId; pcursor is optional for pagination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
