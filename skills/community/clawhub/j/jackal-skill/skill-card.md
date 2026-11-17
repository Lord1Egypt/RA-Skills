## Description:

Sovereign, recoverable memory for AI agents backed by Jackal decentralized storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[regan-milne](https://clawhub.ai/user/regan-milne)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to let an agent save, load, and check usage for encrypted cross-session memory through the Jackal Memory service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may automatically restore and persist sensitive cross-session memory with weak scoping and trust-boundary controls.

Mitigation: Use a dedicated API key, avoid storing credentials or prompt-like behavioral rules in memory blobs, and review memory before enabling automatic load or save behavior.

Risk: The skill depends on private API and encryption keys; exposed keys can disclose or modify stored memory, while lost encryption keys can make memory unrecoverable.

Mitigation: Keep JACKAL_MEMORY_API_KEY and JACKAL_MEMORY_ENCRYPTION_KEY private, back up the encryption key securely, and restrict file and network access to the documented key path and service endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/regan-milne/skills/jackal-skill)
- [Publisher profile](https://clawhub.ai/user/regan-milne)
- [Jackal Memory homepage](https://web-production-5cce7.up.railway.app)
- [Jackal Memory login](https://web-production-5cce7.up.railway.app/auth/login)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JACKAL_MEMORY_API_KEY for service access and a local or environment-provided encryption key for client-side encryption.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
