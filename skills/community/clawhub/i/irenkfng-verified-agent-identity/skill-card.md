## Description:

Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[idraniw29](https://clawhub.ai/user/idraniw29)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agents use this skill to create and manage Billions Network decentralized identities, link an agent DID to a human owner, sign challenges, and verify identity ownership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles long-lived private identity keys and stores sensitive identity data under $HOME/.openclaw/billions.

Mitigation: Review the actual plugin scripts and dependencies before installation, configure BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities, and protect the local identity directory as highly sensitive.

Risk: Importing a private key with --key can expose secret material through command history or process listings.

Mitigation: Avoid importing private keys on the command line unless an operator has reviewed the environment and accepts the exposure risk.

Risk: The security verdict is suspicious because executable artifacts are incomplete for a skill that performs identity operations.

Mitigation: Install only after reviewing the complete scripts and dependencies that will run in the target environment.

## Reference(s):

- [Billions Network](https://billions.network/)
- [ClawHub skill page](https://clawhub.ai/idraniw29/skills/irenkfng-verified-agent-identity)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or text script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; BILLIONS_NETWORK_MASTER_KMS_KEY is optional but recommended before creating identities.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
