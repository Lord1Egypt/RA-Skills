## Description:

Accountability coaching behavior for Nudge that helps agents compose task creation, reminder, completion, failure, and negotiation responses with firm verification-oriented guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neilsanghrajka](https://clawhub.ai/user/neilsanghrajka)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to manage Nudge accountability interactions, including motivational reminders, completion verification, extension requests, cancellations, and failure handling. It is intended for cases where tone, motivation, and judgment about task completion affect whether accountability consequences are triggered.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prompt agents to share detailed proof or failure reasons with third-party accountability targets.

Mitigation: Confirm target recipients and disclosure level before sending proof, failure reasons, private work details, health information, location data, screenshots, secrets, or embarrassing consequences.

Risk: The skill encourages strict accountability decisions that may be inappropriate for emergencies or genuine external blockers.

Mitigation: Apply the documented leniency cases for emergencies, technical failures, first-time users, and honest pre-deadline renegotiation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neilsanghrajka/skills/nudge-coach)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text guidance with command suggestions when task state changes are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Completion and failure messages may include proof or failure reasons that are sent to accountability targets.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
