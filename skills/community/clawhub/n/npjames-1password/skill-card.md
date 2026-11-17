## Description:

Set up and use 1Password CLI (op) for installation, desktop app integration, sign-in, multi-account handling, and secret read, inject, and run workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[npjameszheng1125-netizen](https://clawhub.ai/user/npjameszheng1125-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to install and authenticate the 1Password CLI, confirm account access, and run secret-management commands through a dedicated tmux session while avoiding secret leakage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secret values can be exposed in terminal output, logs, captured tmux panes, or plaintext files when examples print or write secret material.

Mitigation: Control the exact op commands run; avoid printenv, echo, --no-masking, and pane capture after secret-producing commands; prefer op run or op inject without writing secrets to disk.

Risk: Injected secrets or private keys written to disk can remain after the task completes.

Mitigation: Write secret files only when required, use restrictive file permissions, and clean up generated secret files explicitly.

## Reference(s):

- [1Password CLI get-started](https://developer.1password.com/docs/cli/get-started/)
- [Skill reference: get-started](references/get-started.md)
- [Skill reference: op CLI examples](references/cli-examples.md)
- [ClawHub skill page](https://clawhub.ai/npjameszheng1125-netizen/skills/npjames-1password)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires 1Password CLI (op), tmux, and an authenticated 1Password account; no machine-readable output is guaranteed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
