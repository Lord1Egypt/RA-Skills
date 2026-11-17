## Description:

Manage Apple Notes via the `memo` CLI on macOS (create, view, edit, delete, search, move, and export notes).

This skill is ready for commercial/non-commercial use.

## Publisher:

[npjameszheng1125-netizen](https://clawhub.ai/user/npjameszheng1125-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent manage Apple Notes through the `memo` command-line tool on macOS, including creating, listing, searching, editing, deleting, moving, and exporting notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on the third-party `memo` CLI and asks the user to grant access to Apple Notes data.

Mitigation: Verify the `memo` CLI source and publisher before installation, and grant macOS Automation access only when comfortable with that CLI operating on Notes data.

Risk: Supported note operations include viewing, exporting, editing, moving, and deleting notes.

Mitigation: Review selected notes and folders before confirming interactive operations, and revoke Automation permission when the workflow is no longer needed.

## Reference(s):

- [memo GitHub repository](https://github.com/antoniorodr/memo)
- [ClawHub skill page](https://clawhub.ai/npjameszheng1125-netizen/skills/npjames-apple-notes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include macOS-only setup steps, interactive terminal prompts, and Apple Notes Automation permission guidance.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
