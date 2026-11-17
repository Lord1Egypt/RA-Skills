## Description:

Collects daily activity from Linear, Slack, and DM chat, writes a daily journal entry in Notion, and sends a completion DM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[p-take55](https://clawhub.ai/user/p-take55)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to compile a personal end-of-day work journal from Linear, Slack, and DM activity into Notion and notify the configured user when the page is updated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private Slack and DM content may be copied into Notion without enough scoping or confirmation.

Mitigation: Use the skill only with explicit source opt-in, configured Notion destination, and a confirmation step before writing private content.

Risk: The completion notification is directed to a fixed DM recipient in the skill text.

Mitigation: Replace the hard-coded DM identifier with an explicitly configured recipient for the intended user before use.

Risk: Journal entries may include sensitive details from work conversations.

Mitigation: Redact sensitive content before writing to Notion and limit the destination page permissions to the intended audience.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/p-take55/phase1-selfedit-demo/tree/main/skills/notion-daily-journal)
- [ClawHub skill page](https://clawhub.ai/p-take55/skills/notion-daily-journal)

## Skill Output:

**Output Type(s):** [Markdown, Text, Configuration, Guidance]

**Output Format:** [Markdown journal sections plus a short DM notification]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured Notion, Slack, DM chat, and Linear access to gather activity and update the daily journal.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
