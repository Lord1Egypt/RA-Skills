## Description:

Integrates with the macOS Notes app so an agent can create, list, read, update, append, delete, and search Apple Notes through a Node.js CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swancho](https://clawhub.ai/user/swancho)

### License/Terms of Use:

CC-BY-NC-4.0

## Use Case:

Developers and agent users on macOS use this skill to manage Apple Notes from an agent workflow, including creating notes, retrieving note content, appending updates, and searching existing notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Update and delete commands can alter or remove Apple Notes without confirmation.

Mitigation: Read the target note before changing it, keep backups, and avoid using the skill on folders that contain important or sensitive notes unless the action is reviewed.

Risk: Duplicate note titles can cause the skill to operate on the wrong note.

Mitigation: Use a specific folder and unique note titles before running update, append, or delete actions.

Risk: The skill requires access to local Apple Notes through macOS automation.

Mitigation: Install and run it only on trusted macOS systems where Apple Notes automation access is appropriate.

## Reference(s):

- [Mac Notes Agent on ClawHub](https://clawhub.ai/swancho/skills/mac-notes-agent)
- [Publisher profile](https://clawhub.ai/user/swancho)

## Skill Output:

**Output Type(s):** [shell commands, text, configuration]

**Output Format:** [Markdown guidance with shell command examples and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS with Apple Notes, Node.js, and osascript available.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
