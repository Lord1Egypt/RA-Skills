## Description: <br>
Call GET /api/kuaishou/get-video-detail/v2 for Kuaishou Video Details through JustOneAPI with videoId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Kuaishou video details from JustOneAPI for a supplied videoId, then summarize fields such as video URL, caption, and author information for content analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a URL query parameter. <br>
Mitigation: Avoid sharing command output, errors, proxy logs, or diagnostic traces that might include the request URL, and install only when the publisher is trusted with the token. <br>
Risk: The skill requires a sensitive JUST_ONE_API_TOKEN credential. <br>
Mitigation: Pass the token through the documented environment variable or CLI token argument, and do not paste token values into chat messages, screenshots, or logs. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_video_detail&utm_content=project_link) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_video_detail&utm_content=project_link) <br>
- [Kuaishou Video Details operations](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON from the JustOneAPI response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JUST_ONE_API_TOKEN credential and a Kuaishou videoId query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
