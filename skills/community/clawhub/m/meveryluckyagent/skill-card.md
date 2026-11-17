## Description:

Meverylucky AI Agent helps agents create and manage Billions Network decentralized identities, link them to human owners, and generate or verify authentication proofs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meverylucky](https://clawhub.ai/user/meverylucky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create local decentralized identities, link an agent identity to a human owner, and prove or verify identity ownership through signed challenges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived private keys may be stored in plaintext when BILLIONS_NETWORK_MASTER_KMS_KEY is not configured.

Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities and rotate any keys previously stored without encryption.

Risk: Private keys passed on the command line can be exposed through shell history or process inspection.

Mitigation: Prefer generated identities or secure environment/configuration handling instead of passing existing private keys as CLI arguments.

Risk: Identity files under $HOME/.openclaw/billions contain sensitive key and authentication material.

Mitigation: Restrict filesystem access to $HOME/.openclaw/billions and treat signed tokens and challenge records as sensitive.

Risk: Challenge replay protection is weak for signed tokens and challenges.

Mitigation: Use fresh challenges, avoid reusing signed tokens, and review the flow before using the identity outside a test environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/meverylucky/skills/meveryluckyagent)
- [Billions Network](https://billions.network/)
- [README](README.md)
- [Skill Definition](SKILL.md)
- [OpenClaw Environment Documentation](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or text script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Script outputs include DID strings, identity lists, JSON success objects, signed proof tokens, and verification URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
