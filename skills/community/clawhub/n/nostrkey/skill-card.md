## Description:

Cryptographic identity SDK for AI agents that generates Nostr keypairs, signs events, encrypts messages, creates BIP-39 seed phrases, and supports portable backup tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vveerrgg](https://clawhub.ai/user/vveerrgg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create or restore a Nostr identity, persist it as an encrypted local identity file, sign Nostr events, publish to relays, and encrypt direct messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Seed phrases, passphrases, and private keys are high-sensitivity identity secrets and may be exposed if pasted into chat or printed in logs.

Mitigation: Use secure local secret entry, avoid displaying private keys, and treat any seed phrase or passphrase shown in chat or logs as compromised.

Risk: The example workflow saves an identity with the placeholder passphrase change-me.

Mitigation: Replace example passphrases with strong operator-provided secrets before creating or loading identity files.

Risk: The skill can create persistent identity files and publish signed Nostr events over relay connections.

Mitigation: Restrict filesystem and network access, review generated events before publishing, and pin or verify the installed package before relying on the identity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vveerrgg/skills/nostrkey)
- [Project homepage](https://github.com/HumanjavaEnterprises/nostrkey.app.OC-python.src)
- [PyPI package](https://pypi.org/project/nostrkey/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create encrypted identity files and public identity metadata when the operator runs the documented workflows.]

## Skill Version(s):

0.3.0 (source: frontmatter, release evidence, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
