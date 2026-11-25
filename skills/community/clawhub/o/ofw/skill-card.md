## Description:

This skill should be used when the user asks about OurFamilyWizard (OFW) co-parenting data. Triggers on phrases like "check OFW", "OurFamilyWizard inbox", "OFW messages", "OFW calendar", "OFW expenses", "what did my co-parent say", "log an expense in OFW", "OFW journal", or any request involving co-parenting messages, calendar events, shared expenses, or journal entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

People using OurFamilyWizard and their assistants use this skill to retrieve and manage co-parenting messages, calendar events, shared expenses, attachments, and journal entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation phrases may make an ambiguous calendar, expense, or journal request appear to refer to OFW.

Mitigation: Confirm that the user means OurFamilyWizard when the request is ambiguous.

Risk: Opening an unread message can mark it read and expose a First Viewed time; sending messages and changing shared records can have lasting or co-parent-visible effects.

Mitigation: Explain read-status effects before fetching unread message bodies, preview co-parent-visible changes, and obtain explicit user confirmation before sending or deleting records.

## Reference(s):

- [OFW MCP npm package](https://www.npmjs.com/package/ofw-mcp)
- [ofw-mcp project repository (linked in the skill documentation)](https://github.com/chrischall/ofw-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Calendar and expense data]

**Output Format:** [Text and Markdown responses; OFW records and iCalendar files where requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May retrieve, create, or update OFW messages, calendar entries, expenses, and journal entries; attachment and message access can have visibility or read-status effects.]

## Skill Version(s):

2.30.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
