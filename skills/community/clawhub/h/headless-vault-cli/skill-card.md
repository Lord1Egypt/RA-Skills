## Description:

Read and edit Markdown notes on your personal computer via SSH tunnel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[logancyang](https://clawhub.ai/user/logancyang)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to list, read, create, and append Markdown notes in a personal vault through a preconfigured SSH tunnel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SSH command construction can turn untrusted configuration into local command execution.

Mitigation: Review before installing; validate username, host, and port values, avoid unquoted SSH examples, and use safer argv handling before trusting it with a personal notes vault.

Risk: The skill accesses a personal notes vault over an SSH tunnel.

Mitigation: Use the documented forced-command SSH restriction, vault sandboxing, strict host key checking, and non-destructive create/append workflow before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/logancyang/skills/headless-vault-cli)
- [Headless Vault CLI setup instructions](https://github.com/logancyang/headless-vault-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ssh and VAULT_SSH_USER; VAULT_SSH_PORT and VAULT_SSH_HOST are optional.]

## Skill Version(s):

1.2.6 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
