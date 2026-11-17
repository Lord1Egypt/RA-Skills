## Description:

Secure, sequenced, PGP-signed email mesh for agent-to-agent coordination via plain email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zachlagden](https://clawhub.ai/user/zachlagden)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use InterClaw to coordinate OpenClaw agents over ordinary email while adding PGP signing, optional encryption, message sequencing, gap detection, and trusted-fingerprint filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles mailbox credentials, PGP key material, and persistent message archives.

Mitigation: Use a dedicated email account, app-specific credentials or a secret manager, and explicit retention plus file-permission controls for ~/.interclaw.

Risk: Helper commands and downloaded binaries can affect a real mailbox before they are independently reviewed.

Mitigation: Review helper scripts and downloaded binaries before installation, then test with an isolated mailbox before production use.

Risk: Mail providers that rewrite MIME content can break PGP signature verification.

Mitigation: Use providers or self-hosted mail paths that preserve message content, and verify a signed round trip before relying on the channel.

## Reference(s):

- [InterClaw Protocol v3](docs/protocol-v3.md)
- [InterClaw GitHub repository](https://github.com/zachlagden/interclaw)
- [Himalaya v1.1.0 download](https://github.com/pimalaya/himalaya/releases/tag/v1.1.0)
- [ClawHub InterClaw release page](https://clawhub.ai/zachlagden/skills/interclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, environment variable settings, and protocol examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local mail, GPG, and trusted-fingerprint configuration before real mailbox use.]

## Skill Version(s):

0.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
