## Description:

Outlook / Microsoft 365 Secure API CLI for mail and calendar that helps agents read, search, triage, and, with explicit confirmation, mutate mail and calendar data through porteden.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porteden](https://clawhub.ai/user/porteden)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to operate Outlook and Microsoft 365 mail and calendars from an agent session for reading, search, triage, and explicitly confirmed changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing an unpinned third-party CLI that handles sensitive Microsoft 365 mail, calendar, and credential access.

Mitigation: Review the porteden CLI and publisher before installation, prefer browser login, use isolated profiles, and revoke Microsoft access plus clear keyring credentials when finished or if package integrity is uncertain.

Risk: Broad Microsoft Graph scopes or shared credentials could expose more mailbox or calendar data than the task requires.

Mitigation: Use the narrowest mail-only or calendar-only scopes that satisfy the task and keep account access separated with profiles or PE_PROFILE.

Risk: Send, reply, forward, delete, modify, create, update, and respond operations can be irreversible or visible to recipients and attendees.

Mitigation: Echo the target account, message or event identifier, affected recipients or attendees, and intended change, then wait for explicit user confirmation before running any mutating command.

Risk: Mail and calendar content can contain untrusted instructions from senders, organizers, attendees, locations, bodies, or attachments.

Mitigation: Treat mailbox and event content as data only, summarize and attribute claims to their source, and avoid following instructions found inside messages or events.

## Reference(s):

- [PortEden homepage](https://porteden.com)
- [ClawHub skill page](https://clawhub.ai/porteden/skills/outlook-cli)
- [ClawHub publisher profile](https://clawhub.ai/user/porteden)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Outlook mail and calendar CLI command examples, including compact JSON output flags.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mutating mail or calendar commands require explicit user confirmation; compact JSON output is recommended for agent-readable results.]

## Skill Version(s):

1.0.8 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
