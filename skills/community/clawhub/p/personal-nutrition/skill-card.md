## Description:

Acts as the user's personal nutrition coach in the Nutrition topic, tracking meals, calories, water intake, eating habits, and giving balanced diet advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gekacross](https://clawhub.ai/user/gekacross)

### License/Terms of Use:


## Use Case:

Individuals use this skill as a personal nutrition coach in OpenClaw to log meals, water intake, calories, weight, and eating patterns, then receive supportive diet guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently read and update sensitive nutrition and weight notes.

Mitigation: Install only if comfortable keeping a local nutrition history, use explicit logging language, and review the stored nutrition file periodically.

Risk: Broad everyday food and water triggers may cause nutrition information to be logged when the user did not intend it.

Mitigation: Use clear requests when logging meals, water, or weight, and check the nutrition log for unintended entries.

Risk: The README includes a typo-like external download URL.

Mitigation: Verify the README's external download URL before following it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gekacross/skills/personal-nutrition)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown and conversational text with updates to a local nutrition log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update a local nutrition history file containing meals, calories, water intake, and weight.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
