## Description:

Access overseas or external URLs through the JumpOnce proxy service, including HTTP forwarding and WebSocket relay support through an Oracle Cloud Phoenix, USA exit server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[men459](https://clawhub.ai/user/men459)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route HTTP or WebSocket requests through JumpOnce when target websites or APIs are blocked or unreachable from the current network. It is suited to external API access workflows that can tolerate a third-party proxy handling request metadata and response data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send target URLs, request metadata, API keys, and response data through the JumpOnce third-party proxy service.

Mitigation: Use the skill only for approved external requests, avoid proxying secrets, cookies, internal systems, or confidential data, and review target URLs before forwarding.

Risk: The documented JumpOnce API endpoint uses plain HTTP, which can expose proxied data and credentials in transit.

Mitigation: Avoid using the proxy until an HTTPS endpoint is available, or restrict use to non-sensitive data in controlled environments.

Risk: The artifact includes examples that pass API keys on the command line or suggest storing keys in workspace Markdown.

Mitigation: Prefer environment variables or an approved secret manager, and do not place live API keys in shell history, command arguments, or workspace documentation.

Risk: The Python SDK package is installed from an external package source.

Mitigation: Pin and independently review the SDK package before installation in managed environments.

## Reference(s):

- [JumpOnce API Reference](references/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/men459/skills/jump-once-proxy)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API calls]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce proxied HTTP responses or raw passthrough response bytes when using the bundled forwarding script.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
