## Description: <br>
Call GET /api/web/rendered-html/v1 for Web Page Rendered HTML Content through JustOneAPI with url. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to call JustOneAPI's rendered HTML endpoint for a supplied web page URL and receive the rendered page content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends target URLs to JustOneAPI and the security review notes that token and URL handling should be reviewed before installation. <br>
Mitigation: Avoid private, internal, signed, or credential-bearing URLs; provide the API token through the documented environment variable; and prefer a revised version that avoids passing authentication in command arguments or query strings. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web_rendered_html&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web_rendered_html&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-web-rendered-html) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; accepts a required url query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
