## Description:

Set up and use 1Password CLI (op) for installation, desktop app integration, sign-in, and secret read, inject, and run workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shouone](https://clawhub.ai/user/shouone)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure and operate the 1Password CLI safely inside agent workflows, including sign-in, account selection, access checks, and secret injection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples and command output can expose vault secrets in terminal logs, tmux captures, chat, or plaintext files.

Mitigation: Do not print, paste, log, or persist secrets; prefer masked output and `op run` or `op inject` workflows over writing secret material to disk.

Risk: Commands using `--no-masking`, `--out-file`, or ordinary config output paths can leave credentials visible or stored with weak cleanup controls.

Mitigation: Avoid `--no-masking` for real secrets, restrict file permissions before writing secret-derived files, and remove temporary secret material immediately after use.

Risk: Running `op` outside the required tmux session can cause repeated authentication prompts or unstable secret-access workflows.

Mitigation: Use a fresh dedicated tmux socket and session for all `op` commands, verify access with `op whoami`, and terminate the session after the workflow completes.

## Reference(s):

- [1Password CLI get-started](https://developer.1password.com/docs/cli/get-started/)
- [get-started.md](references/get-started.md)
- [cli-examples.md](references/cli-examples.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and operational steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the 1Password CLI binary, a 1Password account, and tmux for command execution workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
