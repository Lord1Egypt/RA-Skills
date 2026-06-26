## Description: <br>
Call GET /api/instagram/get-post-detail/v1 for Instagram Post Details through JustOneAPI with code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch Instagram post details from JustOneAPI by shortcode, then summarize caption, media, publish time, and engagement-oriented fields for analysis or archiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the user's JustOneAPI token and Instagram post shortcode to JustOneAPI. <br>
Mitigation: Use a limited-scope or easily rotated token, keep token values out of chat and logs, and install only when the JustOneAPI service is trusted for the queried data. <br>
Risk: The helper passes credentials as query parameters, which may appear in service or proxy logs. <br>
Mitigation: Avoid sharing command output or request URLs that may contain credentials, and rotate the token if accidental exposure is suspected. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_post_detail&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_post_detail&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-instagram-get-post-detail) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and an Instagram post shortcode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
