## Description:

Chinese-language password utility for generating random passwords, PINs, and passphrases and performing basic password strength checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate passwords, PINs, and passphrases and to run basic password strength checks for routine password management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests read and command-execution access while the security review says its appropriate scope is limited to password, PIN, passphrase generation, and basic strength checking.

Mitigation: Review before installing and run only in a sandboxed agent session where read and command execution are limited to the intended password utility workflow.

Risk: The security review says the artifact overstates its security, audit, vulnerability scanning, breach checking, and automation scope.

Mitigation: Use it only as a local password utility and basic strength checker; do not rely on it for compliance audits, vulnerability scanning, breach detection, or penetration testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/password-gen-pro-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline Python and shell examples plus text and JSON-like command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated passwords, PINs, passphrases, and strength scores should be treated as sensitive output.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
