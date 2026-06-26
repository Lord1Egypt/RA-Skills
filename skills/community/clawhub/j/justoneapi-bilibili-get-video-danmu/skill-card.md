## Description: <br>
Call GET /api/bilibili/get-video-danmu/v2 for Bilibili Video Danmaku through JustOneAPI with aid and cid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to fetch Bilibili video danmaku by AID and CID for audience reaction analysis and subtitle-style comment review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The access token is sent as a query parameter to api.justoneapi.com, so it may appear in full request URLs, logs, screenshots, or error reports. <br>
Mitigation: Use a restricted or easily revocable JUST_ONE_API_TOKEN and avoid sharing logs, screenshots, or full request URLs that may contain the token. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_danmu&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN plus aid and cid; page is optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
