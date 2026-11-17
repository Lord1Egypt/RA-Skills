## Description:

Backup OpenClaw workspace to Git repository (Gitee/GitHub/GitLab).

This skill is ready for commercial/non-commercial use.

## Publisher:

[solidexu](https://clawhub.ai/user/solidexu)

### License/Terms of Use:

Apache 2.0

## Use Case:

External users, developers, and agent operators use this skill to back up OpenClaw workspace documents, memory, and skills to a private Git repository for data safety and migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace backups may upload sensitive OpenClaw documents, memory, and skills to an external Git host.

Mitigation: Use a private repository, review intended backup paths before pushing, and add secret scanning plus an explicit pre-push review before routine use.

Risk: Git access tokens may be exposed through repository remotes, configuration files, shell history, cron entries, or logs.

Mitigation: Use the narrowest possible short-lived token, store it outside the repository, avoid embedding it in cron entries or persistent remotes, and rotate it regularly.

Risk: Automatic watching can trigger backups before path validation and review controls are in place.

Mitigation: Do not enable the watcher until path validation, secret scanning, and explicit pre-push review are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/solidexu/skills/git-backup-publish)
- [Gitee personal access tokens](https://gitee.com/profile/personal_access_tokens)
- [GitHub personal access tokens](https://github.com/settings/tokens)
- [GitLab personal access tokens](https://gitlab.com/-/profile/personal_access_tokens)
- [Gitee user repository API endpoint](https://gitee.com/api/v5/user/repos)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and environment variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute or propose shell scripts that create private Git repositories, copy workspace files, commit changes, push backups, or configure file-change monitoring.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
