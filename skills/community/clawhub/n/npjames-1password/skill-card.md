## Description: <br>
Set up and use 1Password CLI (op) for installation, desktop app integration, sign-in, account selection, and secret read, inject, or run workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npjameszheng1125-netizen](https://clawhub.ai/user/npjameszheng1125-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install and operate the 1Password CLI, authenticate in a dedicated tmux session, choose accounts, and read or inject secrets without placing secret values in chat, logs, or source files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable an agent to access 1Password vault secrets. <br>
Mitigation: Require exact account, vault, item, and field names before secret reads, and avoid unmasked printing of secrets. <br>
Risk: Secret values or generated files may be exposed through pane capture, logs, repositories, or shared folders. <br>
Mitigation: Prefer `op run` or `op inject`, avoid pane capture after secret reads, keep temporary files out of shared locations, use restrictive permissions, delete temporary outputs, and lock 1Password when finished. <br>


## Reference(s): <br>
- [1Password CLI get started](https://developer.1password.com/docs/cli/get-started/) <br>
- [Artifact reference: get-started.md](artifact/references/get-started.md) <br>
- [Artifact reference: cli-examples.md](artifact/references/cli-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/npjameszheng1125-netizen/npjames-1password) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the 1Password CLI binary `op`; preferred workflows use desktop app integration and a fresh dedicated tmux session for all `op` commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
