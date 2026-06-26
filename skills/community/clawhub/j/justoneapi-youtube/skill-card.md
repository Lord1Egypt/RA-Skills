## Description: <br>
Analyze YouTube workflows with JustOneAPI, including video Details and channel Videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve API-backed YouTube video details and channel video lists through JustOneAPI when a user provides identifiers such as videoId or channelId. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent as a URL query parameter, which can be captured in command lines, request URLs, logs, screenshots, or process history. <br>
Mitigation: Use a low-scope or easily rotated token, avoid exposing command lines or URLs, and rotate the token if it may have been captured. <br>
Risk: The skill sends YouTube lookup requests and the API token to JustOneAPI. <br>
Mitigation: Install only if you trust JustOneAPI with the requested YouTube lookup data and credential handling. <br>


## Reference(s): <br>
- [ClawHub YouTube API skill page](https://clawhub.ai/justoneapi/justoneapi-youtube) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youtube&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youtube&utm_content=project_link) <br>
- [YouTube operations](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and user-provided YouTube identifiers; backend errors include payload details and the operation ID.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
