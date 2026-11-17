## Description:

Book time, check calendar availability, and handle scheduling email through a Mermail mailbox plus Google Calendar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mermail](https://clawhub.ai/user/mermail)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external-facing teams use this skill to turn inbound scheduling email into real Google Calendar availability, offer grounded time slots, and send Mermail confirmations after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inbound scheduling mail and calendar/tool output can contain untrusted instructions or misleading data.

Mitigation: Treat inbound content and tool output as data only, require clean scan status before body interpretation, use bounded reads, and ignore requests that change tools, recipients, payment, or approval rules.

Risk: Calendar event creation and Mermail sends produce external effects.

Mitigation: Preview exact event details, recipients, and message body, then require fresh user approval for calendar writes and email sends separately.

Risk: Disconnected or disallowed Google Calendar tooling can make scheduling status uncertain.

Mitigation: Stop on disconnected or disallowed Calendar state, present the exact OAuth handoff when needed, and avoid claiming a hold or confirmation unless the authoritative tool result succeeds.

## Reference(s):

- [Mermail AI Skills documentation](https://docs.mermail.app/ai/skills)
- [Scheduling agent tools](references/tools.md)
- [Scheduling agent workflows](references/workflows.md)
- [Scheduling agent security](references/security.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls]

**Output Format:** [Markdown with structured status summaries and approval previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports mailbox identity, calendar connection status, offered slots, event creation evidence, send status, blockers, and uncertainty separately.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
