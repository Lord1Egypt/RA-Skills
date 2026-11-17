## Description:

Manage Microsoft 365 email, calendar, and contacts through the ms365 CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thecfguy](https://clawhub.ai/user/thecfguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent inspect and manage Microsoft 365 mail, folders, calendar events, recurring meetings, and contacts from a terminal session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad authority to send mail, delete or move messages, and create or delete calendar events.

Mitigation: Require explicit user confirmation before sending mail, deleting or moving messages, creating meetings with attendees, or deleting calendar events.

Risk: The installation guidance recommends an unpinned global ms365 CLI install.

Mitigation: Use a pinned and verified ms365 CLI version where possible before allowing the agent to execute commands.

Risk: Microsoft 365 delegated permissions can expose sensitive mailbox, calendar, and contact data.

Mitigation: Avoid broad delegated permissions and keep authentication revocation or logout available through ms365 auth logout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thecfguy/skills/ms365-cli)
- [ClawHub publisher profile](https://clawhub.ai/user/thecfguy)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-managed ms365 authentication and bounded command results; list operations should not request more than 100 items at once.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
