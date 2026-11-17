## Description:

OpenClaw Backup Rclone helps configure, schedule, run, inspect, and restore OpenClaw backups to rclone-compatible remote storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doradx](https://clawhub.ai/user/doradx)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw operators and developers use this skill to set up recurring or manual backups of OpenClaw configuration, skills, agents, workspaces, memory, and credentials to an rclone remote and to review restore commands when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default backups can include credentials, memory, and workspaces, which may contain sensitive data.

Mitigation: Use only trusted encrypted backup destinations and disable credentials or memory backups unless they are explicitly needed.

Risk: Remote storage choices without strong protection can expose backup contents.

Mitigation: Avoid FTP and prefer encrypted rclone destinations with restricted access.

Risk: Restoring over /root/.openclaw can overwrite the current OpenClaw state.

Mitigation: Take a fresh snapshot first and test restores in a staging directory before extracting over the live directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/doradx/skills/openclaw-backup-rclone)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and backup script invocation parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes options for rclone remote path, retention count, backup scope, and check-only status checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
