## Description:

Complete GitHub passwordless authentication setup using SSH keys and Personal Access Tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happydog-intj](https://clawhub.ai/user/happydog-intj)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to configure GitHub SSH authentication and GitHub CLI Personal Access Token authentication for passwordless Git operations and repository management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to run mutable remote shell code.

Mitigation: Review the scripts locally before installation and avoid curl-to-bash execution.

Risk: The setup flow creates broad, durable GitHub credentials.

Mitigation: Use a fine-grained, short-lived token with only the permissions needed, protect SSH keys with a passphrase, and rotate or revoke credentials when no longer needed.

Risk: Verification commands can create and delete GitHub repositories.

Mitigation: Run account-changing verification only when those changes are intended, preferably against a disposable test repository or account.

## Reference(s):

- [GitHub SSH documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [GitHub CLI manual](https://cli.github.com/manual/)
- [GitHub CLI Linux installation](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional setup and verification shell scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
