## Description:

Secure credential manager using AES-256 (Fernet) encryption. Stores, retrieves, and rotates secrets using a mandatory Master Key. Use for managing API keys, database credentials, and other sensitive tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1999azzar](https://clawhub.ai/user/1999azzar)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to store, retrieve, and list local credentials through a command-line vault protected by a required master key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner characterizes the package as a prototype-style local vault with under-scoped secret handling.

Mitigation: Use it only in private workspaces, avoid high-value credentials until the package is fixed, and review the implementation before deployment.

Risk: Passwords passed as command-line arguments may be exposed through shell history or process listings.

Mitigation: Avoid entering real passwords directly on the command line; prefer a safer secret input path before production use.

Risk: Service names, usernames, and metadata are treated as non-encrypted local data.

Mitigation: Do not store sensitive context in service names, usernames, or metadata, and keep the workspace private.

Risk: Vault access depends on the strength and handling of MEMA_VAULT_MASTER_KEY.

Mitigation: Use a strong master key, inject it through a secure environment mechanism, and never store it in plaintext on disk.

## Reference(s):

- [Mema Vault security policy](references/security-policy.md)
- [Mema Vault ClawHub release page](https://clawhub.ai/1999azzar/skills/mema-vault)
- [Publisher profile](https://clawhub.ai/user/1999azzar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include masked credential values by default; raw secrets can be displayed only when the --show flag is used.]

## Skill Version(s):

1.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
