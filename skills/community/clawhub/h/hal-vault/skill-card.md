## Description:

hal-vault helps agents store, find, rotate, and use local encrypted secrets while keeping outputs masked by default and revealing values only to feed requested commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofoxai](https://clawhub.ai/user/ofoxai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage API keys, tokens, passwords, SSH keys, and related credentials in a local SSH-key-encrypted vault. The skill guides safe storage, masked search/list workflows, rotation/removal, and secret injection into requested commands without printing raw secret values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw secrets could be exposed if an agent prints revealed values or writes already-substituted commands into chat, logs, or files.

Mitigation: Use masked outputs for conversation and documentation; reserve --reveal for feeding a requested process and refuse to paste raw values.

Risk: A revealed secret can appear in the process argument list when command substitution lands inside a command argument.

Mitigation: Prefer environment variables or stdin for secret injection; use arguments only as a disclosed last resort.

Risk: Vault data or the SSH key could be mishandled during project setup.

Mitigation: Keep .hal-vault out of version control, store the SSH key outside the project tree, and protect the key material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ofoxai/skills/hal-vault)
- [ClawHub publisher profile](https://clawhub.ai/user/ofoxai)
- [hal-vault skill homepage](https://github.com/ofoxai/skills/tree/main/skills/hal-vault)
- [hal-vault CLI reference](references/cli-reference.md)
- [hal-vault CLI repository](https://github.com/ofoxai/hal-vault)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Masked-by-default handling guidance; raw secrets should not be printed into chat, logs, files, or command arguments.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
