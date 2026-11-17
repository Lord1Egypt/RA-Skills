## Description:

A decentralized identity management toolkit for AI agents using the iden3 protocol on Billions Network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louise2364](https://clawhub.ai/user/louise2364)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and manage Billions Network DIDs for agents, link an agent DID to a human owner, and verify identity ownership with signed challenges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates, imports, persists, and uses agent identity signing keys, and private keys may be stored in plaintext if encryption is not configured.

Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities, store the master key securely, and restrict permissions on $HOME/.openclaw/billions.

Risk: Passing real private keys as command-line arguments can expose secrets through shell history or process inspection.

Mitigation: Avoid passing real private keys on the command line; prefer generated identities or a secure secret-handling path.

Risk: Signed challenges may be reused if freshness and replay protection are not enforced by the surrounding workflow.

Mitigation: Use unique, short-lived challenges and add replay protection before relying on signed challenges as fresh authentication.

Risk: The skill interacts with external DID and Billions Network services during identity and attestation flows.

Mitigation: Review the expected network domains before deployment and require explicit user consent for wallet or attestation interactions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/louise2364/skills/ntala-ai-2047)
- [Billions Network](https://billions.network/)
- [OpenClaw Environment Documentation](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces DIDs, identity records, challenges, signed proof status, verification URLs, and identity verification results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
