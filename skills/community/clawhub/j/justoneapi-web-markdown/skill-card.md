## Description:

Call GET /api/web/markdown/v1 for Web Page Markdown Content through JustOneAPI with url.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch Markdown content for a supplied web page URL through the JustOneAPI web markdown endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs are sent to JustOneAPI and may be visible in service-side URL logs.

Mitigation: Avoid sensitive or signed URLs unless sharing them with JustOneAPI is acceptable.

Risk: The JustOneAPI token can be exposed through local process metadata because it is passed as a command-line argument.

Mitigation: Use a narrowly scoped, revocable token and rotate it if command history or process metadata may have been exposed.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web_markdown&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web_markdown&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summary with optional raw JSON from the API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a URL input and a JUST_ONE_API_TOKEN credential.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
