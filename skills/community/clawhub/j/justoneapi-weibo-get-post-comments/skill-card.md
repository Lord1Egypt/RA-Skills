## Description: <br>
Call GET /api/weibo/get-post-comments/v1 for Weibo Post Comments through JustOneAPI with mid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch Weibo post comment data from JustOneAPI for a specific post mid, including text, authors, timestamps, sorting, and pagination support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent to api.justoneapi.com as a URL query parameter and may be exposed in command logs, request URLs, telemetry, or shared screenshots. <br>
Mitigation: Use a limited-scope token if available, avoid sharing command logs or full request URLs, and rotate the token if it may have appeared in logs or telemetry. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-weibo-get-post-comments) <br>
- [JustOneAPI API Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_post_comments&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_post_comments&utm_content=project_link) <br>
- [Generated Operations Reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with an inline Node command and JSON API response output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a Weibo post mid; optional sort and maxId parameters control ordering and pagination.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
