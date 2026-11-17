## Description:

Checks and updates OpenClaw skills installed from GitHub git clones, limited to skill directories that retain .git metadata and an origin remote.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viccwang](https://clawhub.ai/user/viccwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to check whether GitHub-cloned local skills are behind their origin remotes and to update branch or tag based installs when the repository state is safe.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change installed skill code by pulling or checking out updates from remote repositories.

Mitigation: Run the check command first, verify the origin remote and expected update for each skill, and keep backups of local changes before updating.

Risk: Bulk updates can apply changes from multiple repositories before each change has been reviewed.

Mitigation: Avoid bulk updates for untrusted repositories; update one skill at a time after reviewing the reported status and pending diff.

Risk: Local changes, ahead commits, or diverged history can be overwritten or complicated by an update workflow if ignored.

Mitigation: Treat dirty, ahead, diverged, and unsupported reports as stop conditions and resolve the repository state manually before retrying.

## Reference(s):

- [README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/viccwang/skills/github-skill-updater)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports repository status values such as up-to-date, update-available, dirty, ahead, diverged, unsupported, and updated.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
