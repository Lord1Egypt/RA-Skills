## Description:

Manage Microsoft To Do tasks via the `todo` CLI, including task creation, listing, completion, deletion, subtasks, notes, and list organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[underwear](https://clawhub.ai/user/underwear)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to have an agent manage Microsoft To Do tasks and lists through the `todo` command-line interface. It is suited for creating, updating, completing, deleting, filtering, and organizing tasks when Microsoft Azure OAuth access has been configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The third-party CLI receives access to the user's Microsoft To Do account.

Mitigation: Review the CLI before installing, verify or pin the package version, and only connect accounts whose To Do data can be safely managed by this tool.

Risk: Microsoft app credentials and OAuth tokens are stored in local plaintext files.

Mitigation: Protect `keys.yml` and token files with owner-only file permissions, use short-lived or rotated Azure client secrets, and remove stale tokens when access is no longer needed.

Risk: Task and list deletion commands can bypass interactive confirmation.

Mitigation: Require explicit user confirmation before running any deletion command and prefer stable task IDs over names or indexes for destructive operations.

## Reference(s):

- [Microsoft To Do Skill Page](https://clawhub.ai/underwear/skills/microsoft-todo)
- [Setting Up Microsoft API Access](references/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill expects structured CLI output via `--json` where supported.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
