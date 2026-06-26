## Description: <br>
Call GET /api/twitter/get-user-posts/v1 for Twitter User Published Posts through JustOneAPI with restId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch published posts for a specific X/Twitter user through JustOneAPI using a required restId, with optional pagination support for longer timelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token to call the endpoint. <br>
Mitigation: Run it in a trusted local environment and avoid sharing command logs, screenshots, or output that may expose the token. <br>
Risk: Endpoint responses may include account monitoring data and engagement details for Twitter/X posts. <br>
Mitigation: Review returned JSON before sharing it and handle the results according to the user's privacy, compliance, and data-use requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-twitter-get-user-posts) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_twitter_get_user_posts&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_twitter_get_user_posts&utm_content=project_link) <br>
- [Generated Operations Reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, JSON] <br>
**Output Format:** [Markdown guidance with a shell command example and JSON API response output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and a Twitter/X user restId; cursor is optional for pagination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
