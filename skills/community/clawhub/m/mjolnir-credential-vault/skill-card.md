## Description:

GPG AES-256 encrypted credential management for storing, retrieving, listing, and removing passwords, API tokens, and secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[king6381](https://clawhub.ai/user/king6381)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation authors use this skill to add encrypted local credential storage and retrieval to scripts or agent workflows without hardcoding passwords, API tokens, or other secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell helper has a code-injection risk when handling untrusted service or field names.

Mitigation: Prefer the Python CLI or API path, and do not pass untrusted service or field names to the Bash helper until it passes arguments as data rather than interpolating them into Python source.

Risk: A long-lived CRED_MASTER_PASS environment variable can expose the master password to same-user processes on some systems.

Mitigation: Use interactive entry, gpg-agent, a secrets manager, or session-scoped runtime injection instead of storing the master password in persistent shell configuration.

Risk: Retrieved secrets are printed in plaintext.

Mitigation: Limit command output exposure, avoid logging get command results, and handle returned values only in the consuming process that needs them.

## Reference(s):

- [Credential Vault ClawHub release page](https://clawhub.ai/king6381/skills/mjolnir-credential-vault)
- [Gpg4win](https://gpg4win.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print retrieved secrets in plaintext when the get operations are used.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
