## Description:

AI agent for local businesses to automate appointment scheduling, reminders, cancellations, and calendar integration.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[dotdance](https://clawhub.ai/user/dotdance)

### License/Terms of Use:

MIT

## Use Case:

Local business operators can use this agent as a chat-based appointment scheduling demo for booking, cancellation, rescheduling, and showing hours or services. It is suitable for evaluating an appointment workflow before adding production consent, storage, calendar, and messaging controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The demo collects scheduling details such as names and phone numbers without built-in consent, privacy notices, retention controls, or secure storage.

Mitigation: Add explicit consent, privacy notices, secure storage, and deletion or retention controls before using it for real customer bookings.

Risk: Calendar or messaging integrations could request broader access than needed if added for production use.

Mitigation: Use least-privilege calendar and messaging scopes and review those scopes before deployment.

Risk: Appointments are stored only in memory in the demo, so booking data is not durable across restarts.

Mitigation: Use durable, access-controlled storage before relying on the agent for actual appointments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dotdance/skills/local-business-appointment-agent)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and console interaction text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included Node.js demo stores appointments in memory and does not configure external calendar, messaging, or credentialed services by default.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
