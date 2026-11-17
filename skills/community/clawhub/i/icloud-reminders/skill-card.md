## Description:

Manage Apple iCloud Reminders via CloudKit API for listing, adding, completing, deleting, and organizing reminders, lists, and hierarchical subtasks with 2FA-protected accounts via cached sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarekbecker](https://clawhub.ai/user/tarekbecker)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to manage Apple iCloud Reminders from an agent-assisted workflow, including creating, editing, completing, deleting, searching, syncing, and exporting reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unaudited mutable third-party Homebrew binary that handles Apple ID credentials and reusable iCloud sessions.

Mitigation: Install only if the Homebrew tap and CLI publisher are trusted, review the package before use, and prefer interactive authentication or an OS credential store over plaintext credential files.

Risk: The documented commands can modify or delete iCloud Reminders and can export reusable session archives.

Mitigation: Review proposed commands before execution, protect session.json and exported session archives like login secrets, and avoid sharing exported sessions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tarekbecker/skills/icloud-reminders)
- [iCloud Reminders CLI Homepage](https://github.com/tarekbecker/icloud-reminders-cli)
- [ClawHub Publisher Profile](https://clawhub.ai/user/tarekbecker)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide use of CLI commands that read, create, update, complete, delete, sync, export, or import iCloud Reminders data and sessions.]

## Skill Version(s):

0.1.6 (source: server release metadata; artifact frontmatter says 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
