## Description:

HTTP status code reference for instant offline lookup of status code meanings, common causes, and fix suggestions across RFC-standard, WebDAV, Nginx, Cloudflare, and common unofficial codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to interpret HTTP response codes, compare related errors, and choose practical debugging or retry actions while working offline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTP troubleshooting guidance can be incomplete for provider-specific or unofficial status codes.

Mitigation: Verify high-impact production changes against the relevant service, proxy, or standards documentation before applying them.

Risk: Retry recommendations can increase load or duplicate side effects when used blindly.

Mitigation: Use exponential backoff, respect Retry-After headers, and retry only idempotent or otherwise safe requests.

Risk: Authentication and authorization debugging may prompt users to discuss secrets or tokens.

Mitigation: Avoid pasting credentials into agent conversations and rotate any secret that may have been exposed.

## Reference(s):

- [HTTP Status Codes Complete Reference](references/codes.md)
- [ClawHub Skill Page](https://clawhub.ai/tobewin/skills/http-status)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown with concise explanations, comparison summaries, and retry guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline reference output; no API calls, network access, persistence, or credential handling.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
