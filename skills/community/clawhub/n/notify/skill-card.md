## Description:

Configure notification channels and conditional alerts while tracking what is watched and what has been sent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to choose notification channels, timing, formatting, batching, and escalation behavior for agent-generated notifications. It helps agents avoid notification fatigue while still surfacing urgent events promptly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real notification integrations can send messages through the wrong channel or at the wrong time if account preferences are misconfigured.

Mitigation: Confirm notification channels, timezone, quiet hours, and critical-alert preferences before enabling real SMS, push, email, or chat delivery.

Risk: Poor batching or escalation choices can create notification fatigue.

Mitigation: Use the skill's batching, quiet-hours, and escalation limits, including stopping after three critical-alert attempts unless the user explicitly authorizes more.

## Reference(s):

- [ClawHub Skill: Notify](https://clawhub.ai/ivangdavila/skills/notify)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with examples, checklists, and routing tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Notification guidance includes channel-specific length limits, quiet-hours behavior, batching thresholds, and escalation limits.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
