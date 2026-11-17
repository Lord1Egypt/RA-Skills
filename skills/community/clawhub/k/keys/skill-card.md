## Description:

Secure API key management with broker. Keys never exposed to agent context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure and operate a local broker that makes authenticated API calls to preconfigured services without exposing decrypted API keys to the agent context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Key-management instructions can expose plaintext API keys.

Mitigation: Use tightly scoped API keys, avoid verification commands that print secrets, and do not place real keys in command-line arguments.

Risk: The broker grants broad authenticated API access to allowed services.

Mitigation: Review broker requests before execution and require explicit user approval before destructive or financial API actions.

## Reference(s):

- [Keys ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/keys)
- [Keys Setup](artifact/setup.md)
- [Key Management](artifact/manage.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, JSON request examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for local keychain-backed API calls and broker management; broker command output is JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
