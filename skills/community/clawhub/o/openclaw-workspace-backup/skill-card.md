## Description: <br>
Backs up configured local git workspaces to GitHub branches from .env-defined workspace paths and can report workspace backup status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangpengle](https://clawhub.ai/user/zhangpengle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run unattended backups of multiple local git workspaces to dedicated remote branches, then inspect status and recent backup logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform unattended git commits and pushes for every configured workspace, and the security review notes insufficient destination validation or safeguards. <br>
Mitigation: Before enabling it, inspect every WORKSPACE_<id> path, run git remote -v in each repository, and confirm origin points to a dedicated private backup remote. <br>
Risk: Configured repositories may contain local files or secrets that would be included in backup commits. <br>
Mitigation: Review .gitignore and local workspace contents for secrets before running backups. <br>
Risk: The --force option can rewrite remote branch history. <br>
Mitigation: Avoid --force unless you are prepared to rewrite the remote backup branch history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangpengle/openclaw-workspace-backup) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Python package metadata](artifact/pyproject.toml) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Configuration guidance] <br>
**Output Format:** [Command-line output and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured WORKSPACE_<id> paths and git remotes; may commit and push repository changes.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
