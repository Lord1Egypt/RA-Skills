## Description:

Manage Things 3 via the `things` CLI on macOS by adding or updating projects and todos through the URL scheme and reading, searching, or listing data from the local Things database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to help an agent manage Things 3 tasks on macOS, including reading inbox, today, upcoming, projects, areas, and tags, and adding or updating todos through the `things` CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned third-party `things3-cli` install target.

Mitigation: Prefer a pinned and reviewed version of the dependency before deployment.

Risk: The Things database can contain sensitive personal or business task data and may require broad Full Disk Access.

Mitigation: Grant Full Disk Access only when necessary, limit it to the calling app, and remove the permission afterward.

Risk: Write operations can modify Things 3 todos and projects.

Mitigation: Use `--dry-run` for write previews when practical and review commands before execution.

Risk: Authentication tokens used for update operations can be exposed through shell history or command logs.

Mitigation: Avoid placing tokens directly in command history and prefer environment-based handling where appropriate.

## Reference(s):

- [things3-cli GitHub repository](https://github.com/ossianhempel/things3-cli)
- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/skills/mh-things-mac)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and Things CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose read and write operations against a local Things 3 database; write operations should use dry-run previews when practical.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
