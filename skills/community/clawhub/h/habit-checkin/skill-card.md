## Description:

Habit Checkin tracks daily habit check-ins, including current streak, best streak, and total check-in days.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to record daily habit check-ins and view habit streak statistics during agent conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Habit check-ins may be stored persistently in a local JSON file.

Mitigation: Review the configured storage path before use and delete the local habit_streaks.json file when retained check-in history is no longer needed.

Risk: Broad trigger phrases such as check-in and sign-in language may activate the skill unintentionally.

Mitigation: Prefer the explicit habit-checkin trigger when installing or invoking the skill.

Risk: Unrelated Bilibili learning notes can make the skill documentation harder to interpret.

Mitigation: Remove unrelated video notes from deployment copies when cleaner documentation is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/habit-checkin)
- [Habit Loop learning resource](https://www.bilibili.com/video/BV1kLUxYBEUK)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Natural-language check-in status with local JSON streak data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist habit streak history in a local habit_streaks.json file.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
