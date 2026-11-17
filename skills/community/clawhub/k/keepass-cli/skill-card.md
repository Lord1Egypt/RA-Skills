## Description:

A JSON CLI for creating and managing local KeePass (.kdbx) databases, including entries, groups, and attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beocca](https://clawhub.ai/user/beocca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to manage local KeePass vaults through structured JSON commands for database creation, inspection, entries, groups, and attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad read and write access to a password vault.

Mitigation: Use a dedicated or low-risk KeePass database unless broad vault authority is intentional and reviewed.

Risk: Credential handling can leak secrets through plaintext environment files, command lines, logs, or explicit secret-output flags.

Mitigation: Avoid plaintext .env storage where possible, avoid passing real passwords or OTP seeds on command lines, and treat --show-secrets and --include-data output as sensitive.

Risk: Permanent delete operations can bypass the KeePass recycle-bin safety net.

Mitigation: Use --permanent only after confirming irreversible deletion is intended.

Risk: Unpinned dependencies can change behavior or security posture over time.

Mitigation: Pin python-dotenv and pykeepass versions for serious or production use.

## Reference(s):

- [pykeepass documentation](artifact/pykeepass_docs.html)
- [pykeepass GitHub repository](https://github.com/libkeepass/pykeepass)
- [ClawHub skill page](https://clawhub.ai/beocca/skills/keepass-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command contracts and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return one JSON object per invocation with stable error codes; secrets and attachment data require explicit flags.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
