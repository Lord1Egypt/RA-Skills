## Description:

Backup/restore OpenClaw config and workspace via git.

This skill is ready for commercial/non-commercial use.

## Publisher:

[burnlife001](https://clawhub.ai/user/burnlife001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to back up and restore OpenClaw configuration and workspace directories with Git-based shell scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups can upload OpenClaw configuration and workspace data to the default third-party Git destination if the configuration is not changed.

Mitigation: Configure the Git host, organization, branch, and repository names for a trusted destination before running backup commands.

Risk: Restore operations can remove local files in existing target directories before pulling content.

Mitigation: Run restore only after creating an independent backup or in a clean target directory where replacing local files is acceptable.

Risk: Git backup commands may commit files that contain private configuration or workspace data.

Mitigation: Inspect the staged files and review ignore rules before committing or pushing a backup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/burnlife001/skills/openclaw-gitbak)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command examples and shell configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides backup and restore commands that can initialize Git repositories, commit files, push to a configured remote, clone repositories, and pull restored content.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
