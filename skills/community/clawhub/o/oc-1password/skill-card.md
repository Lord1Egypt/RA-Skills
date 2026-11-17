## Description:

Set up and use 1Password CLI for sign-in, desktop integration, and reading or injecting secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and authenticate the 1Password CLI, select an account, and read or inject secrets for command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An example disables output masking and prints a database password, which could expose the secret in output or retained logs.

Mitigation: Avoid the unmasked example; keep output masking enabled and pass secrets directly to the command or configuration that needs them without printing them.

Risk: Security analysis was partial because a local path-like reference could not be resolved, so the evidence is incomplete.

Mitigation: Review the referenced material and inspect commands before installing or using the skill.

## Reference(s):

- [1Password CLI get started](https://developer.1password.com/docs/cli/get-started/)
- [get-started.md](references/get-started.md)
- [cli-examples.md](references/cli-examples.md)
- [ClawHub skill page](https://clawhub.ai/hillstreet-ph/skills/oc-1password)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover sign-in, account selection, secret reads, command execution, and configuration injection.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
