## Description:

MCP server for OurFamilyWizard that provides read/write access to messages, calendar events, expenses, and journal entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External OurFamilyWizard users use this skill to let an agent inspect and manage co-parenting messages, calendar events, shared expenses, and journal entries. It is intended for workflows where the user wants OFW data access through MCP while preserving explicit review for sensitive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run external MCP server code with reusable OFW credentials and broad read/write access to sensitive legal-family records.

Mitigation: Use a pinned, reviewed package version, keep OFW credentials out of project files and shell history, and store secret files with restrictive permissions.

Risk: Some OFW operations can send messages, delete records, mark messages read, or update last-seen status.

Mitigation: Require explicit user confirmation before sending messages, deleting records, reading unread messages that may mark them read, or calling notification reads that update status.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chrischall/skills/ofw-mcp)
- [npm Package](https://www.npmjs.com/package/ofw-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide MCP tool calls that read or modify OurFamilyWizard records.]

## Skill Version(s):

2.11.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
