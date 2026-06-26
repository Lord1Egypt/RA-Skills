## Description: <br>
Call GET /api/weibo/get-user-video-list/v1 for Weibo User Video List through JustOneAPI with uid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to retrieve a Weibo user's video-list data through JustOneAPI for a supplied Weibo UID, with optional cursor-based pagination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required JustOneAPI token is handled in exposure-prone places, including a command-line argument and the API request URL. <br>
Mitigation: Use the skill only in trusted environments, avoid exposing tokens in chat messages or logs, prefer a revision that reads the token directly from the environment, and rotate the token if it may have been logged or shared. <br>
Risk: Running the skill sends the requested Weibo UID and any pagination cursor to api.justoneapi.com. <br>
Mitigation: Confirm that sharing those identifiers with JustOneAPI is acceptable for the user's privacy and compliance requirements before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-weibo-get-user-video-list) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_user_video_list&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with an executable Node.js command and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; expected inputs are uid and optional cursor.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
