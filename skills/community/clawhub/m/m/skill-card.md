## Description:

Short alias skill for moving files, directories, or data; also for system management like managing services or packages. Use when relocating or reorganizing content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlang-cn](https://clawhub.ai/user/openlang-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill as a compact command reference for moving or reorganizing files and directories, managing packages and services, and planning data migration tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides broad administrative and destructive command patterns, including recursive deletion, package changes, service changes, database restore, and remote Git deletion.

Mitigation: Require explicit user confirmation before executing destructive commands, and verify exact paths, package names, service names, database targets, and remote refs before use.

Risk: The one-letter trigger can make high-impact administrative guidance easy to invoke from vague requests.

Mitigation: Treat generated commands as reviewable proposals and ask for clarification when the request does not specify the intended target and outcome.

Risk: Move and synchronization examples can overwrite, delete, or relocate important data if applied to the wrong source or destination.

Mitigation: Prefer non-destructive flags, dry runs where supported, backups, and destination checks before using commands such as rm -r or rsync --delete.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell command examples and concise procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
