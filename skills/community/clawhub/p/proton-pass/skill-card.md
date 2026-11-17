## Description:

Manage Proton Pass vaults, items, passwords, SSH agent integration, and secret injection into applications through Proton Pass CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kakatkarakshay](https://clawhub.ai/user/kakatkarakshay)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage Proton Pass vaults, credentials, SSH keys, password generation, secret references, and application secret injection from an agent-assisted CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer examples can execute unverified remote code.

Mitigation: Prefer a package-manager installation or a verified, pinned installer before running setup commands.

Risk: Temporary passphrase-free SSH private keys can expose credentials.

Mitigation: Avoid copying private keys into /tmp; when temporary files are unavoidable, keep permissions strict and securely remove them immediately.

Risk: Generated secret files can be left readable by unintended users.

Mitigation: Keep generated secret files at 0600 or stricter.

Risk: Unmasked output or long-lived environment variables can leak secrets.

Mitigation: Avoid --no-masking and long-lived environment-variable secrets except in tightly controlled automation.

Risk: Auto-created SSH identities can sync keys into an unintended vault or socket.

Mitigation: Use auto-create SSH identities only with a dedicated vault and SSH agent socket intended for synchronization.

## Reference(s):

- [ClawHub Proton Pass CLI skill page](https://clawhub.ai/kakatkarakshay/skills/proton-pass)
- [Proton Pass CLI macOS/Linux installer](https://proton.me/download/pass-cli/install.sh)
- [Proton Pass CLI Windows installer](https://proton.me/download/pass-cli/install.ps1)
- [Proton Pass account security settings](https://account.proton.me/pass/security)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell, PowerShell, JSON, YAML, and environment-variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may retrieve, inject, or store secrets and should be reviewed before execution.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
