## Description:

Integrates an agent with local macOS Reminders to list, add, edit, delete, complete, and suggest reminders from meeting notes across multiple languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swancho](https://clawhub.ai/user/swancho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users on macOS use this skill to let an assistant manage local Reminders items, including list-specific tasks, priorities, recurrence, and user-approved reminders suggested from meeting notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A non-EventKit add-reminder path constructs executable AppleScript from reminder text, so crafted titles or notes could trigger unintended local commands.

Mitigation: Install only if comfortable granting local Reminders access, avoid adding reminders from untrusted copied text until the AppleScript construction path is fixed, or route additions through EventKit.

Risk: Delete and complete commands modify live Reminders data that may sync across Apple devices.

Mitigation: Review delete and complete requests carefully and confirm the target reminder ID before executing changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/swancho/skills/mac-reminders-agent)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS Reminders permission for reminder operations; meeting-note parsing is local text processing.]

## Skill Version(s):

1.4.0 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
