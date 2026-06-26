## Description: <br>
Backs up OpenClaw workspace files to a private Git repository on Gitee, GitHub, GitLab, or a self-hosted Git server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solidexu](https://clawhub.ai/user/solidexu) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create a private Git repository, run manual workspace backups, and optionally configure automatic backup checks for core OpenClaw files, memory, and skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy OpenClaw memory, identity, user, and skill files to a Git remote. <br>
Mitigation: Use a dedicated private repository with a least-privilege token and confirm the intended backup contents before running the scripts. <br>
Risk: Automatic watcher, heartbeat, cron, or daemon use may upload workspace changes without a manual review step. <br>
Mitigation: Review or disable automatic watcher behavior before enabling heartbeat, cron, or daemon mode. <br>
Risk: The backup script includes a force-push fallback that can overwrite remote history. <br>
Mitigation: Review or remove force-push behavior before using the skill with an existing repository. <br>
Risk: Changing BACKUP_DIR can affect where files are staged and removed during backup preparation. <br>
Mitigation: Do not override BACKUP_DIR unless it points to an isolated path intended only for backup staging. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/solidexu/git-backup-publish) <br>
- [Gitee repository creation API](https://gitee.com/api/v5/user/repos) <br>
- [Gitee personal access tokens](https://gitee.com/profile/personal_access_tokens) <br>
- [GitHub personal access tokens](https://github.com/settings/tokens) <br>
- [GitLab personal access tokens](https://gitlab.com/-/profile/personal_access_tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with bash commands and shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces repository setup, manual backup, and watcher configuration guidance for OpenClaw workspace backups.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
