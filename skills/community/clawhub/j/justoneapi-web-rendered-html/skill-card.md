## Description:

Call GET /api/web/rendered-html/v1 for Web Page Rendered HTML Content through JustOneAPI with url.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch rendered HTML content for a specified web page URL through the JustOneAPI rendered-html endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through process arguments or URL logs.

Mitigation: Use a revocable, narrowly scoped token if available, avoid logging command arguments or request URLs, and rotate the token if exposure is possible.

Risk: Submitted URLs are sent to JustOneAPI and may reveal private targets or embedded secrets.

Mitigation: Use the skill only with URLs you are comfortable sharing with JustOneAPI, and avoid URLs containing secrets, private session data, or sensitive query strings.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web_rendered_html&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web_rendered_html&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-web-rendered-html)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Markdown summary followed by raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a target url parameter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
