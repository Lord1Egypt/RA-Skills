## Description:

Moyu Journal Auto records workplace-activity journal entries, summarizes daily and weekly downtime totals, and produces humorous reports or work-log style summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swiftuis](https://clawhub.ai/user/swiftuis)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this entertainment and personal journaling skill to record local workplace-activity notes, calculate daily or weekly totals, and generate either humorous summaries or work-log style text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store workplace-activity notes in local journal files that can contain sensitive personal or employment information.

Mitigation: Use a dedicated local journal directory, review stored entries regularly, and avoid recording confidential workplace details.

Risk: Optional browser history, calendar, and broad filesystem access can expose more private context than the journal needs.

Mitigation: Keep optional history and calendar access disabled unless required, and grant filesystem access only to the intended journal path where the agent platform supports scoped permissions.

Risk: The artifact claims local or encrypted storage, but the server security guidance says the encryption design is unclear or unsupported.

Mitigation: Treat the stored journal as plaintext-like unless the publisher provides verifiable encryption, retention, and deletion controls.

Risk: Work-log style summaries could be misleading if reused as formal workplace reporting.

Mitigation: Review and edit generated summaries before sharing them, and do not present fictionalized activity as verified work records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/swiftuis/skills/moyu-journal-auto)
- [Publisher profile](https://clawhub.ai/user/swiftuis)
- [Publisher homepage](https://x.com/walletgonegirl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with local JSON journal entries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or write local journal files under ~/.openclaw/moyu-journal/ and may use chat history, browser history, or calendar data when those permissions are enabled.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
