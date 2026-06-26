## Description: <br>
Obsidian Sync CLI for syncing vaults on headless Linux servers with full end-to-end encryption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bpauli](https://clawhub.ai/user/bpauli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill as a command reference for configuring and running obsync to synchronize Obsidian vaults on headless Linux systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes commands that handle Obsidian account credentials and end-to-end encryption passwords. <br>
Mitigation: Avoid storing real passwords in shared shell history or reusable environment files; use the configured keyring behavior deliberately. <br>
Risk: Pull, push, watch, and service commands can change local or remote vault contents. <br>
Mitigation: Verify the vault name and local path, and make a backup before the first sync or before enabling background synchronization. <br>
Risk: The workflow depends on an upstream third-party CLI running on the user's machine. <br>
Mitigation: Install only when the upstream obsync CLI and the execution environment are trusted. <br>


## Reference(s): <br>
- [Obsync ClawHub page](https://clawhub.ai/bpauli/obsync) <br>
- [obsync upstream repository](https://github.com/bpauli/obsync) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown command reference with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional JSON-output and verbose-logging flags for the upstream CLI.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
