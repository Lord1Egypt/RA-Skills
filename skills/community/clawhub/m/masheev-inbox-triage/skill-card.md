## Description:

Triage a Masheev customer inbox from an AI assistant connected to the Masheev MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masheev](https://clawhub.ai/user/masheev)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners and support leads use the skill to review inbox conversations, identify cases needing human attention, and organize internal assignments, statuses, tags, or notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrectly selected conversations or workspace permissions could lead to unintended changes to internal conversation records.

Mitigation: Confirm the connected workspace and OAuth permissions, then review proposed assignments, status changes, tags, and notes before authorizing them.

Risk: Customer messages may be processed by the connected AI host and can contain personal information.

Mitigation: Read only what is needed for triage and avoid copying personal data into summaries or internal notes unless necessary.

## Reference(s):

- [Masheev agent documentation](https://docs.masheev.com/agents)
- [ClawHub skill listing](https://clawhub.ai/masheev/skills/masheev-inbox-triage)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Inbox summaries and proposed action lists in natural language]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Internal conversation records may be changed only after user authorization; the skill does not send customer replies.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
