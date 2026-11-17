## Description:

Helps users set up a dependency-free Python TOTP viewer on Linux to register secrets and display one-time codes locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maebahesioru](https://clawhub.ai/user/maebahesioru)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and developers can set up a local Linux command-line viewer for TOTP codes and register or remove authenticator secrets, including when moving accounts from a phone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sharing a Google Authenticator export QR code or decoded migration payload with an agent can expose every included 2FA secret.

Mitigation: Decode and import export QR codes entirely on the user's own machine; never send the QR, payload, or full secrets to an agent or chat.

Risk: The viewer stores TOTP seeds in a local plaintext file, which can be exposed if the file or backups are accessible to others.

Mitigation: Use it only when local plaintext storage is acceptable; restrict the secrets file to the user's account and protect copies and backups.

## Reference(s):

- [Local TOTP Viewer release](https://clawhub.ai/maebahesioru/skills/local-totp-viewer)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Guidance]

**Output Format:** [Markdown with a Python code block and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local TOTP codes from user-provided secrets; does not supply the secrets.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
