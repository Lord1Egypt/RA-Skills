## Description: <br>
Call GET /api/youku/get-video-detail/v1 for YOUKU Video Details through JustOneAPI with videoId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call JustOneAPI's YOUKU video detail endpoint with a videoId, then summarize and return video metadata such as title, description, and engagement fields for lookups or dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token can be exposed if request URLs, command logs, screenshots, or shared traces include credential-bearing requests. <br>
Mitigation: Use a least-privilege JUST_ONE_API_TOKEN, avoid sharing request URLs or logs, and rotate the token if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-youku-get-video-detail) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku_get_video_detail&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, JSON] <br>
**Output Format:** [Markdown summary with raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a videoId.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
