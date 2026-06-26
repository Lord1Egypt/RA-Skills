## Description: <br>
Calls JustOneAPI's TikTok post detail endpoint to fetch video, author, description, and related post metadata for a supplied post ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve TikTok post details through JustOneAPI when they need post metadata for content analysis, performance review, or influencer evaluation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token is sent to api.justoneapi.com as a URL query parameter, which can expose it through logs, screenshots, terminal output, or error reports. <br>
Mitigation: Use the skill only with a trusted JustOneAPI account, avoid sharing request URLs or logs, and rotate JUST_ONE_API_TOKEN if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-tiktok-get-post-detail) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_post_detail&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_post_detail&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON returned from the API helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, JUST_ONE_API_TOKEN, and a TikTok postId; the helper calls the documented GET endpoint and returns the parsed response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
