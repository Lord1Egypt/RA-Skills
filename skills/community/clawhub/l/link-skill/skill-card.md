## Description:

Universal API integration skill for enterprise platforms. Connect to any platform using Swagger/OpenAPI discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use LinkSKILL to configure, discover, authenticate against, and call Swagger/OpenAPI-based enterprise platform APIs from CLI-driven workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable credentials may be exposed through local cache output or logs.

Mitigation: Use non-production credentials, avoid --show-cache, rotate any token printed in logs, and add redaction plus stricter cache file permissions before trusted use.

Risk: Authenticated headers can be attached to arbitrary HTTP requests when a full URL is supplied with a configured authenticated platform.

Mitigation: Avoid --url with authenticated platform configs and restrict execution to trusted endpoints until destination allowlisting is added.

Risk: The request executor supports state-changing HTTP methods without an explicit destructive-action confirmation step.

Mitigation: Review each target endpoint and payload before execution, use minimal test payloads first, and add confirmation controls for destructive methods.

## Reference(s):

- [LinkSKILL release page](https://clawhub.ai/hgvgfgvh/skills/link-skill)
- [Publisher profile](https://clawhub.ai/user/hgvgfgvh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include API endpoint listings, request and response schema summaries, command invocations, token-cache status, HTTP status codes, and response snippets.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
