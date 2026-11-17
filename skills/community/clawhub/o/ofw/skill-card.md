## Description:

This skill should be used when the user asks about OurFamilyWizard (OFW) co-parenting data. Triggers on phrases like "check OFW", "OurFamilyWizard inbox", "OFW messages", "OFW calendar", "OFW expenses", "what did my co-parent say", "log an expense in OFW", "OFW journal", or any request involving co-parenting messages, calendar events, shared expenses, or journal entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to help users access OurFamilyWizard co-parenting messages, calendar events, expenses, and journal entries. It supports reviewing records, preparing drafts, and making requested updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential setup may expose an OFW username and password in a project configuration file; the security scan was partial and could not establish that the artifact is safe.

Mitigation: Use a private credential method, keep credential files out of version control, and review the unresolved scan scope before installation.

Risk: Opening an unread inbox message may mark it read and record a visible First Viewed time.

Mitigation: Check whether the message is cached first; pass allowMarkRead:false when it must remain unread, and get user approval before opening it.

## Reference(s):

- [OFW MCP package](https://www.npmjs.com/package/ofw-mcp)
- [OFW skill release page](https://clawhub.ai/chrischall/skills/ofw)

## Skill Output:

**Output Type(s):** [Text, API calls, Configuration, Shell commands]

**Output Format:** [Natural-language summaries, MCP tool calls, and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive family communications and records; some operations change shared OFW data.]

## Skill Version(s):

2.29.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
