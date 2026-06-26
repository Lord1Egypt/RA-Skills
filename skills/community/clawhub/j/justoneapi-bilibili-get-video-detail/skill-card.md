## Description: <br>
Call GET /api/bilibili/get-video-detail/v2 for Bilibili Video Details through JustOneAPI with bvid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Bilibili video metadata from JustOneAPI by BVID and summarize fields such as title, tags, publishing time, engagement metrics, and uploader information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required JustOneAPI token is sent as a URL query parameter, which can expose it through logs or shared command output. <br>
Mitigation: Use a scoped token when available, avoid sharing command output that may include request URLs, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-bilibili-get-video-detail) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_detail&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands] <br>
**Output Format:** [Markdown summary followed by raw JSON from the API helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and a Bilibili bvid; no request body is documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
