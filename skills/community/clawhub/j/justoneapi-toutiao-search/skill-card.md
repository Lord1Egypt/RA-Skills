## Description:

Call 2 search versions for Toutiao App Keyword Search through JustOneAPI with keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run Toutiao app and web keyword searches through JustOneAPI for topic discovery, trend research, and monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-token exposure through command-line and URL-query handling.

Mitigation: Treat JUST_ONE_API_TOKEN as a secret, avoid pasting token values into chat or logs, and use a scoped or disposable token where possible.

Risk: Toutiao search keywords are sent to api.justoneapi.com and may be sensitive or regulated.

Mitigation: Avoid sensitive or regulated keywords unless authorized, and review organizational data-handling requirements before use.

Risk: Command lines and full request URLs may be logged by local tooling or infrastructure.

Mitigation: Sanitize logs and avoid workflows that persist full URLs containing token or query values.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao_search&utm_content=project_link)
- [Toutiao Search API ClawHub Page](https://clawhub.ai/justoneapi/skills/justoneapi-toutiao-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown summary with endpoint details and raw JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and sends keyword query parameters to api.justoneapi.com.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
