## Description: <br>
Backup and restore OpenClaw configuration, agents, sessions, and workspace to and from a private Git repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DarinRowe](https://clawhub.ai/user/DarinRowe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to manually back up local OpenClaw state to a trusted private Git repository, migrate a setup to another machine, or restore a previous OpenClaw state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup may copy sensitive OpenClaw state, including configuration, sessions, memory, and workspace data, into the configured Git repository. <br>
Mitigation: Use only a trusted private repository, verify the repository URL before running the scripts, and add explicit exclusions or encryption for secrets and session material. <br>
Risk: Restore pulls repository contents into the live OpenClaw directory and then runs local package installation and OpenClaw repair commands. <br>
Mitigation: Restore only from a repository and commit you trust, inspect the backup diff before restoring, and avoid running restore from unreviewed branches or remotes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DarinRowe/openclaw-backup-restore) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and script execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces backup and restore actions that read OpenClaw configuration and operate on local OpenClaw state through Git, rsync, npm, and OpenClaw CLI commands.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
