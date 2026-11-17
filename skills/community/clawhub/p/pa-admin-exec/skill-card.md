## Description:

Generates exec-support outputs (plan, prioritized tasks, comms drafts, meeting prep/follow-ups). USE WHEN you want a personal assistant to triage requests and produce ready-to-send drafts and schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kowl64](https://clawhub.ai/user/kowl64)

### License/Terms of Use:


## Use Case:

Employees and executive-support users use this skill to turn messages, calendar availability, task lists, and meeting notes into triage summaries, plans, prioritized tasks, communication drafts, and meeting follow-ups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages, calendar availability, and notes may contain sensitive personal or business information.

Mitigation: Provide only the information you are comfortable sharing with the assistant.

Risk: Drafts or schedule proposals may be inaccurate when timezone or scheduling constraints are missing.

Mitigation: State the timezone and scheduling constraints explicitly before relying on proposed times.

Risk: Generated communications and schedules are proposals, not final actions.

Mitigation: Review all drafts and schedule options before sending, booking, or relying on them.

## Reference(s):

- [PA Output JSON Schema](references/pa-output-json-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/kowl64/skills/pa-admin-exec)
- [Publisher Profile](https://clawhub.ai/user/kowl64)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown pack with a matching structured JSON block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are drafts and proposals only; the skill does not send messages or book meetings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
