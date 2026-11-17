## Description:

Use Keeper Commander CLI and Keeper Secrets Manager workflows when installing Keeper tooling, setting up profiles, signing in, running Keeper interactively, searching vault or admin data, retrieving a specific secret or field, injecting secrets into commands, creating or updating Keeper records, or troubleshooting Keeper terminal sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keeper-security](https://clawhub.ai/user/keeper-security)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and administrators use this skill to work with Keeper Commander CLI and Keeper Secrets Manager tasks such as setup, authentication, vault or admin lookup, field retrieval, secret injection, record updates, and troubleshooting terminal sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keeper workflows can expose sensitive vault data or raw secrets if broad records are dumped or command output is pasted without filtering.

Mitigation: Inspect metadata first, retrieve only the exact requested fields, summarize outputs that may contain sensitive values, and prefer Keeper Secrets Manager injection over displaying secrets.

Risk: Destructive Keeper operations can delete, clear, or remove data from a vault or admin context.

Mitigation: Require explicit user confirmation before delete, clear, or remove operations.

Risk: Interactive login, MFA, and device approval can lose session state across isolated shell calls.

Mitigation: Use a fresh tmux session for interactive Keeper work and hand control to the user for manual authentication steps when needed.

## Reference(s):

- [Keeper Agent Kit reference](references/keeper-agent-kit.md)
- [Keeper documentation entry points](references/keeper-docs.md)
- [Keeper Agent Kit repository](https://github.com/Keeper-Security/keeper-agent-kit)
- [Keeper Docs home](https://docs.keeper.io)
- [Keeper Secrets Manager overview](https://docs.keeper.io/en/keeperpam/secrets-manager/overview)
- [Commander CLI command reference](https://docs.keeper.io/en/keeperpam/commander-cli/command-reference)
- [Keeper notation](https://docs.keeper.io/en/keeperpam/secrets-manager/about/keeper-notation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tmux session commands, Keeper CLI or KSM command suggestions, and secret-handling cautions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
