## Description:

Provides agent guidance for controlling a running Obsidian desktop app through Obsidian's built-in CLI, covering note operations, search, tasks, metadata, plugins, sync, publish, themes, bases, and developer tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[douglascorrea](https://clawhub.ai/user/douglascorrea)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and agents operating with user approval use this skill to read, write, search, organize, and administer an Obsidian vault through the running desktop app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad live control over Obsidian can change, delete, overwrite, restore, or publish vault content.

Mitigation: Require explicit user approval before destructive, overwrite, restore, or publish commands, and keep backups or sync history available.

Risk: Plugin, theme, snippet, and restricted-mode commands can change the user's Obsidian execution environment.

Mitigation: Confirm the requested environment change with the user before running plugin, theme, snippet, or restricted-mode commands.

Risk: Developer-tool commands such as eval, CDP, debugger, DOM access, and screenshots can expose private vault or application state.

Mitigation: Run developer-tool commands only after explicit approval and limit captured output to the user's stated task.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/douglascorrea/skills/obsidian-remote)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that read, modify, publish, debug, or administer a live Obsidian vault.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
