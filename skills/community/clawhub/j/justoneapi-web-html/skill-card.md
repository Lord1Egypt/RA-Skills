## Description:

Call GET /api/web/html/v1 for Web Page HTML Content through JustOneAPI with url.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch the HTML content of a supplied web page URL through JustOneAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs and fetched page content are sent to JustOneAPI.

Mitigation: Avoid private or internal URLs and use the skill only when sharing the requested URL and fetched page content with JustOneAPI is acceptable.

Risk: The JustOneAPI token is placed in a query string.

Mitigation: Use a scoped or disposable token where possible and avoid exposing command lines, logs, screenshots, or process metadata that may contain query-string tokens.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web_html&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web_html&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown summary with an inline shell command and raw JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses operation htmlV1 on /api/web/html/v1 and echoes the requested URL scope before summarizing results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
