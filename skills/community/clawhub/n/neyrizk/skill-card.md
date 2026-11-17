## Description:

Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carolin3-neyzr](https://clawhub.ai/user/carolin3-neyzr)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to create and manage decentralized agent DIDs, link them to human owners, sign identity challenges, and verify DID ownership proofs on the Billions Network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent DID signing keys and can store them as plaintext when BILLIONS_NETWORK_MASTER_KMS_KEY is not set.

Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities and review local key storage before deployment.

Risk: Private keys passed on the command line can be exposed through shell history or process inspection.

Mitigation: Avoid passing private keys with command-line arguments; use an approved secret-handling path for deployment.

Risk: Identity linking requests may be sent to Billions-hosted services.

Mitigation: Use the skill only when the agent is intended to own persistent DIDs and external identity-linking traffic is acceptable.

## Reference(s):

- [Billions Network](https://billions.network/)
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment)
- [ClawHub skill page](https://clawhub.ai/carolin3-neyzr/skills/neyrizk)
- [Publisher profile](https://clawhub.ai/user/carolin3-neyzr)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and may use optional BILLIONS_NETWORK_MASTER_KMS_KEY for key encryption.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
