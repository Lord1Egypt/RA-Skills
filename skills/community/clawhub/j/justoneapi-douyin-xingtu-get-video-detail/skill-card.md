## Description: <br>
Call GET /api/douyin-xingtu/get-video-detail/v1 for Douyin Creator Marketplace (Xingtu) Video Details through JustOneAPI with detailId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a focused JustOneAPI endpoint that retrieves Douyin Creator Marketplace (Xingtu) video detail data by detailId for content review and integration compatibility workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required JustOneAPI token is sent as a URL query parameter and may be captured by infrastructure logs. <br>
Mitigation: Keep JUST_ONE_API_TOKEN in the agent environment, avoid sharing request URLs or logs, and rotate the token if exposure is suspected. <br>
Risk: The skill sends Douyin video detail IDs to JustOneAPI. <br>
Mitigation: Install and run it only when the user trusts JustOneAPI with the token and submitted video detail IDs. <br>


## Reference(s): <br>
- [Endpoint Operations Reference](generated/operations.md) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_video_detail&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu-get-video-detail) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Short Markdown summary followed by raw JSON from the JustOneAPI endpoint] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a detailId; endpoint errors include the backend payload and operation ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
