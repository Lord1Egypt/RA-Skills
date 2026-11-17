## Description:

Gmail: Show unread inbox summary (sender, subject, date).

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Google Workspace users and agents assisting them use this skill to review unread Gmail inbox items by sender, subject, and date without modifying the mailbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose unread Gmail message metadata from a mailbox.

Mitigation: Install only where gws Gmail read access is acceptable and review the shared gws authentication and security guidance when available.

Risk: Authentication and global security behavior are delegated to a separate shared gws skill.

Mitigation: Confirm the shared gws skill is present and reviewed before relying on this triage helper.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-gmail-triage)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default command output is a table; JSON output is available through the gws format option.]

## Skill Version(s):

1.0.12 (source: release metadata; skill metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
