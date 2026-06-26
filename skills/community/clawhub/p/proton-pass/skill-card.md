## Description: <br>
Manage Proton Pass vaults, items, passwords, SSH agent integration, and secret injection workflows through Proton Pass CLI guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KakatkarAkshay](https://clawhub.ai/user/KakatkarAkshay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and operators use this skill to work with Proton Pass CLI for vault and item management, SSH key workflows, password generation, TOTP access, and secret injection into commands or templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes commands that can view, share, delete, transfer, import, or inject sensitive Proton Pass secrets and SSH keys. <br>
Mitigation: Require explicit user approval before running destructive, sharing, transfer, SSH-key import, item-viewing, or secret-injection commands. <br>
Risk: Plaintext credential environment variables and rendered secret files can expose sensitive values through logs, shell history, or committed files. <br>
Mitigation: Prefer file-based credential inputs, keep secret masking enabled, avoid committing rendered files, and do not log resolved secrets. <br>
Risk: Installer commands fetched from remote URLs can introduce supply-chain risk if the source is not verified. <br>
Mitigation: Verify the installer source or use a trusted package manager before installing Proton Pass CLI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KakatkarAkshay/proton-pass) <br>
- [Proton Pass CLI install script for macOS and Linux](https://proton.me/download/pass-cli/install.sh) <br>
- [Proton Pass CLI install script for Windows](https://proton.me/download/pass-cli/install.ps1) <br>
- [Proton Pass account security settings](https://account.proton.me/pass/security) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and CLI usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-facing operational guidance; commands may affect secrets, vault contents, SSH keys, and local configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
