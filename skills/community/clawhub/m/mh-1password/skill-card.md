## Description:

Set up and use 1Password CLI (op) for installing the CLI, enabling desktop app integration, signing in, and reading, injecting, or running secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install, authenticate, and operate the 1Password CLI. It helps manage account sign-in, desktop app integration, and secret access workflows through op commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can expose real passwords or keys in terminal output and local files.

Mitigation: Review commands before execution, avoid printing secrets, keep masking enabled, and prefer flows that do not write secret material to disk.

Risk: Agent-operated 1Password CLI access can affect sensitive accounts and vault data.

Mitigation: Use the skill only in an isolated, permission-scoped environment with planned cleanup and explicit account selection.

Risk: Terminal pane capture after secret output can retain sensitive values.

Mitigation: Do not capture panes or logs after secret output, and close or clean the session after sensitive commands complete.

## Reference(s):

- [1Password CLI get-started documentation](https://developer.1password.com/docs/cli/get-started/)
- [1Password CLI get-started summary](references/get-started.md)
- [op CLI examples](references/cli-examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tmux-based command sequences and secret-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
