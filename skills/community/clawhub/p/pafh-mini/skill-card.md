## Description:

PAHF-Memory helps agents apply a continual personalization loop that clarifies ambiguous preferences, retrieves local preference memory, and integrates user feedback into persistent preference records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welkeyever](https://clawhub.ai/user/welkeyever)

### License/Terms of Use:


## Use Case:

Agents and users use this skill to personalize assistant behavior by clarifying preferences before action, consulting local preference files, and updating preference records after feedback. It is intended for workflows where persistent preference memory is useful and the user consents to local storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local memory and profile files and writes persistent preference records.

Mitigation: Install only when persistent preference storage is acceptable, keep activation narrow, and review memory files regularly.

Risk: The skill may log inferred user habits without clear per-update consent.

Mitigation: Require confirmation for automatic daily observations or disable those updates unless they are explicitly needed.

Risk: Preference memory can include contacts, locations, schedules, or other personal context.

Mitigation: Avoid storing personal details unless they are necessary and explicitly approved by the user.

## Reference(s):

- [Preference Memory Schema Definition](references/preference-schema.md)
- [PAFH-Memory ClawHub skill page](https://clawhub.ai/welkeyever/skills/pafh-mini)
- [Learning Personalized Agents from Human Feedback](https://arxiv.org/abs/2602.16173)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown preference records and conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local memory files when consent and policy conditions are met.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
