## Description: <br>
Call GET /api/instagram/get-user-posts/v1 for Instagram User Published Posts through JustOneAPI with username. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve published Instagram post data for a specified username through JustOneAPI. It supports monitoring recent publishing activity and building an auditable record of post codes, captions, and media types. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a sensitive JustOneAPI token and requested Instagram usernames to api.justoneapi.com. <br>
Mitigation: Use a revocable token, avoid logging command lines or URLs that contain the token, and rotate the token if exposure is suspected. <br>
Risk: API results may contain third-party social media content that needs contextual review before operational use. <br>
Mitigation: Review the returned JSON and summarize only fields relevant to the user's stated monitoring, auditing, or analysis task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-instagram-get-user-posts) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_user_posts&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_user_posts&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON from the API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN; accepts a required username and optional pagination token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
