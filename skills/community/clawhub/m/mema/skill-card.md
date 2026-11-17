## Description:

Mema's personal brain - SQLite metadata index for documents and Redis short-term context buffer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1999azzar](https://clawhub.ai/user/1999azzar)

### License/Terms of Use:


## Use Case:

Developers and agents use Mema Brain to maintain a local SQLite metadata index for workspace documents and a Redis-backed short-term context buffer for ephemeral session state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Redis memory can be configured to use a remote service without built-in authentication or TLS.

Mitigation: Use a local or strongly protected Redis instance, and add network controls, authentication, and encrypted transport before pointing REDIS_HOST at any remote service.

Risk: Short-term mental state may contain sensitive or instruction-like content.

Mitigation: Avoid storing secrets or instruction-like content in mental state, and clear keys when the state is no longer needed.

Risk: The Redis dependency is specified with a lower bound rather than a pinned production version.

Mitigation: Pin and review the Redis client version before production deployment.

## Reference(s):

- [Mema Brain on ClawHub](https://clawhub.ai/1999azzar/skills/mema)
- [Publisher profile](https://clawhub.ai/user/1999azzar)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory-management guidance and commands for SQLite metadata indexing and Redis-backed short-term state.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
