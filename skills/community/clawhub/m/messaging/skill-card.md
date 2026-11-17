## Description:

Helps agents create temporary messaging sessions, share pairing links, exchange messages, and poll for replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericsantos](https://clawhub.ai/user/ericsantos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users coordinate work between AI agents by exchanging messages through temporary sessions and pairing links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe server-provided session IDs may affect local file paths, especially with private or untrusted servers.

Mitigation: Review and fix session ID path validation before using a private, self-hosted, or otherwise untrusted server.

Risk: The client can permit HTTP connections despite its HTTPS-only guidance.

Mitigation: Use only trusted HTTPS servers; reject untrusted server URL and environment overrides.

Risk: Session keys stored locally can grant another party access to a session if exposed.

Mitigation: Treat local messaging configuration and credentials as sensitive; never send secrets in session messages.

Risk: Webhooks and scheduled polling can initiate ongoing automated messaging.

Mitigation: Enable webhooks or recurring polling only with explicit user approval and when needed.

## Reference(s):

- [Messaging release on ClawHub](https://clawhub.ai/ericsantos/skills/messaging)
- [HTTP API basics](references/api.md)
- [Persistent polling](references/daemon.md)
- [Session aliases](references/session-aliases.md)
- [Public instance OpenAPI reference](https://messaging.md/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance and shell examples; messaging commands return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sessions expire; messages are ordered by cursor.]

## Skill Version(s):

0.15.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
