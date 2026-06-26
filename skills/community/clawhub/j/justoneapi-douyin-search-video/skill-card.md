## Description: <br>
Call GET /api/douyin/search-video/v4 for Douyin (TikTok China) Video Search through JustOneAPI with keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and analysts use this skill to search Douyin video results through JustOneAPI by keyword, with optional filters for sort order, publish time, duration, page, and search ID. It supports content discovery, trend research, and competitive monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token and search keywords are sent to JustOneAPI, and the token is placed in the request URL query string. <br>
Mitigation: Use a limited or revocable token where available, avoid exposing full request URLs in logs or screenshots, and rotate the token if it may have been shared. <br>
Risk: The skill requires sensitive credentials through JUST_ONE_API_TOKEN. <br>
Mitigation: Provide the token through the environment or command line at runtime and do not paste token values into chat messages, screenshots, or shared logs. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_search_video&utm_content=project_link) <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-douyin-search-video) <br>
- [Publisher profile](https://clawhub.ai/user/justoneapi) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with raw JSON results and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a JustOneAPI token and keyword query parameters; returns backend JSON after an endpoint-specific summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
