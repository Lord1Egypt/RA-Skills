## Description: <br>
Automatically backup OpenClaw configuration to a private GitHub repository with API key sanitization, activity detection, smart backup frequency, and recovery guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wang5sheng](https://clawhub.ai/user/wang5sheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure backups of local OpenClaw configuration, workspaces, memory, credentials, and agent history to a private GitHub repository for migration or disaster recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups can include sensitive OpenClaw configuration, memory, credentials, sessions, and workspaces even though API keys in openclaw.json are sanitized. <br>
Mitigation: Use a new empty private repository, review exactly which files will be uploaded, and add exclusions for secrets, credentials, session data, and workspaces that should not leave the machine. <br>
Risk: The scripts use force-push behavior and remove nested .git directories during initial backup, which can overwrite remote history or remove repository metadata under ~/.openclaw. <br>
Mitigation: Review and edit the scripts before installation, remove force-push behavior, and remove recursive .git deletion unless the target directory has been backed up and inspected. <br>
Risk: The installer changes global Git user.name and user.email settings. <br>
Mitigation: Prefer repository-local Git configuration or manually restore global Git settings after installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wang5sheng/openclaw-github-backup) <br>
- [GitHub new repository page](https://github.com/new) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash commands and bundled shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs backup and activity-check scripts that operate on ~/.openclaw and a user-provided private GitHub repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
