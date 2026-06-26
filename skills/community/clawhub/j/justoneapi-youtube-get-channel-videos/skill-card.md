## Description: <br>
Call GET /api/youtube/get-channel-videos/v1 for YouTube Channel Videos through JustOneAPI with channelId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve videos for a specific YouTube channel through the JustOneAPI endpoint, including support for cursor-based pagination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required JustOneAPI token is passed through command arguments and included in the request URL. <br>
Mitigation: Use a dedicated low-privilege token, avoid environments that log command lines or full URLs, and prefer a revised version that reads credentials from a protected environment variable or secret store if the API supports it. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youtube_get_channel_videos&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-youtube-get-channel-videos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands] <br>
**Output Format:** [Markdown summary with the raw JSON API response when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires channelId and a JustOneAPI token; cursor is optional for pagination.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
