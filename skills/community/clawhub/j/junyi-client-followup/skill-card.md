## Description:

A monthly child development planning follow-up workflow that sends parent questionnaires, collects replies, formats the feedback, and forwards it to the planner without evaluating progress or changing planning reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuanranc](https://clawhub.ai/user/xuanranc)

### License/Terms of Use:

MIT-0

## Use Case:

External Chinese-speaking parents and child development planners use this skill to run monthly check-ins for children ages 0-8, collect parent observations, and route formatted feedback to the planner. It is designed for collection and handoff, not assessment, diagnosis, strategy changes, or report editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles sensitive child and family feedback and may forward parent replies to a planner.

Mitigation: Use only in a controlled parent and planner process where parents know their replies may be forwarded, and route feedback only to the intended planner contact.

Risk: The planning document metadata boundary may be too broad or unclear.

Mitigation: Keep plan metadata in a fixed boundary or separate state store, and require plan_id confirmation before sending questionnaires or processing replies.

Risk: Parent replies can include high-risk safety, medical, emotional, or family-change information.

Mitigation: Avoid public or group display, minimize or redact sensitive feedback when possible, and escalate red-line replies to the planner without adding analysis or advice.

## Reference(s):

- [Client Questionnaire](references/client-questionnaire.md)
- [Client Rules](references/client-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/xuanranc/skills/junyi-client-followup)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and plain-language messages with structured feedback blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes questionnaire prompts, parent confirmations, planner notifications, and state-update guidance; excludes independent assessment or diagnosis.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
