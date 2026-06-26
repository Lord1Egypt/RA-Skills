## Description: <br>
Manage Apple iCloud Reminders via CloudKit API. Use for listing, adding, completing, deleting reminders, managing lists, and hierarchical subtasks. Works with 2FA-protected accounts via cached sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tarekbecker](https://clawhub.ai/user/tarekbecker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage Apple iCloud Reminders through the `reminders` CLI, including listing, creating, editing, completing, deleting, and exporting reminders. It is useful when reminder operations need to be performed from an agent workflow while preserving user control over authentication and destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Apple account credentials and reusable iCloud session files. <br>
Mitigation: Prefer interactive authentication or protected environment variables, avoid plaintext password storage when possible, and protect `~/.config/icloud-reminders/session.json`. <br>
Risk: Exported session archives can grant access equivalent to an authenticated session. <br>
Mitigation: Treat any `session.tar.gz` export as sensitive material and avoid sharing or storing it insecurely. <br>
Risk: Reminder commands can complete, delete, or bulk-edit user data. <br>
Mitigation: Require confirmation before allowing an agent to run destructive or bulk reminder operations. <br>
Risk: Installation depends on a third-party Homebrew tap and CLI project. <br>
Mitigation: Install only after trusting the publisher, tap, and CLI source identified in the release metadata. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tarekbecker/icloud-reminders) <br>
- [iCloud Reminders CLI Homepage](https://github.com/tarekbecker/icloud-reminders-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and CLI output references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke the `reminders` CLI, which can produce human-readable lists or JSON exports depending on the command.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata; artifact frontmatter states 0.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
