## Description:

Manage TOTP/2FA codes locally (add/list/remove accounts, display current codes, and optional Tkinter GUI). Use when a user asks to generate a TOTP code, store a new base32 secret, list 2FA accounts, or manage a local OTP vault from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ordsbot](https://clawhub.ai/user/ordsbot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage a local TOTP vault, add, list, and remove accounts, and display current 2FA codes through a CLI or optional Tkinter GUI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles long-lived 2FA seeds in a local JSON vault.

Mitigation: Review before installing for real accounts, restrict access to the vault file, and avoid shared or synced vault locations.

Risk: Entering TOTP seeds on the command line can expose secrets through shell history or process inspection.

Mitigation: Avoid entering real seeds on the command line when possible, and prefer safer entry methods or an encrypted password manager for important accounts.

Risk: A local TOTP manager may not provide the protections of an OS-backed authenticator or encrypted password manager.

Mitigation: Prefer an encrypted password manager or OS-backed authenticator for high-value accounts.

## Reference(s):

- [ClawHub Otpforge skill page](https://clawhub.ai/ordsbot/skills/otpforge)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Plain text and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce time-sensitive TOTP codes and local vault updates when commands are run.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
