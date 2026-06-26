## Description: <br>
Call GET /api/bilibili/get-video-comment/v2 for Bilibili Video Comments through JustOneAPI with aid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch Bilibili video comment data through JustOneAPI by AID, then summarize comment text, commenter profile fields, and like signals for sentiment analysis or moderation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token and sends it to api.justoneapi.com as part of the endpoint call. <br>
Mitigation: Keep the token in the JUST_ONE_API_TOKEN environment variable, avoid exposing command lines or logs that contain token-bearing URLs, and rotate the token if exposure is suspected. <br>
Risk: API responses may include user-generated comment content and commenter profile fields. <br>
Mitigation: Review returned data before sharing it externally and apply the consuming application's privacy and moderation policies. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_comment&utm_content=project_link) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_comment&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-bilibili-get-video-comment) <br>
- [Generated operation documentation](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON from the API response when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN; the required non-token query parameter is aid, with optional cursor pagination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
