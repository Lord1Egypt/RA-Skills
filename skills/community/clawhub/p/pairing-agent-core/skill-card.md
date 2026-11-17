## Description:

Pairing Agent Core helps agents create and manage Billions Network decentralized identities, link them to human owners, and sign or verify DID challenges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilhant-34](https://clawhub.ai/user/ilhant-34)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to create local Billions Network DIDs, link agent identities to human owners, and prove or verify DID ownership through signed challenges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and persists long-lived identity private keys under $HOME/.openclaw/billions.

Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities and run the skill under an isolated user or profile.

Risk: Existing private keys can be supplied through the --key argument, which may expose secrets through shell history or process listings.

Mitigation: Avoid importing existing wallets with --key and do not pass real tokens or keys directly in shell commands.

Risk: Identity linking and verification sends traffic to Billions services and resolver.privado.id.

Mitigation: Review the external-service trust boundary before installation and use the skill only where those network calls are acceptable.

## Reference(s):

- [Pairing Agent Core on ClawHub](https://clawhub.ai/ilhant-34/skills/pairing-agent-core)
- [Billions Network](https://billions.network/)
- [OpenClaw Environment Documentation](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON, and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local command guidance and script outputs for identity creation, linking, signing, and verification.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
