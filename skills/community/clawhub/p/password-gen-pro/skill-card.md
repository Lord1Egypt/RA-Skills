## Description:

Password Generator helps an agent generate passwords, PINs, passphrases, API-style tokens, username ideas, and password-strength guidance while keeping settings local and avoiding storage of generated passwords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkpareek0315](https://clawhub.ai/user/mkpareek0315)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent for password, PIN, passphrase, username, token-generation, and password-strength assistance. It is best suited for local guidance and credential ideas rather than production credential issuance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan notes that the skill asks the agent to invent passwords and tokens without evidence of a real cryptographic random generator.

Mitigation: Use generated credentials as ideas only; for production credentials, use a password manager or CSPRNG-backed utility and rotate any credential exposed in chat.

Risk: The skill is designed to analyze credential text, which may lead users to paste real passwords into chat.

Mitigation: Avoid entering real credentials; test representative examples or use a trusted local password-manager audit feature for real accounts.

Risk: The skill requests local read and write access for settings and generation statistics.

Mitigation: Review the skill before installing and keep file access limited to the documented local settings path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mkpareek0315/skills/password-gen-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text responses with occasional JSON settings snippets and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated passwords and tokens are displayed to the user and are not intended to be stored by the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
