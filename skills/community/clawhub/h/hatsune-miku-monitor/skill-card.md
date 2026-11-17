## Description:

Hatsune Miku Monitor provides a desktop GTK system monitor with an animated character, system status panel, edge hiding, opacity control, and a one-click cleanup action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1173910773](https://clawhub.ai/user/1173910773)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and desktop users can use this skill to install and run a local animated system monitor that displays CPU, memory, disk, and temperature information. It also provides setup, dependency, GIF asset, and autostart guidance for the monitor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The one-click boost action can make disruptive local system changes, including altering cache or swap behavior, pruning logs, deleting user caches, or closing browser renderer processes.

Mitigation: Review the cleanup behavior before use, keep monitoring read-only where possible, and require explicit confirmation before running cleanup actions.

Risk: Passwordless sudoers setup for cleanup commands increases the impact of accidental or unwanted execution.

Mitigation: Avoid the passwordless sudoers instructions unless the administrator has reviewed and accepted the exact commands and scope.

Risk: Autostart configuration can run the desktop monitor and cleanup-capable UI automatically on login.

Mitigation: Enable autostart only when the user intentionally wants persistent startup behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1173910773/skills/hatsune-miku-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with Python, shell, and systemd configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill includes local desktop-monitor scripts and setup guidance; no external API credentials are described in the evidence.]

## Skill Version(s):

1.0.1 (source: server release metadata, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
