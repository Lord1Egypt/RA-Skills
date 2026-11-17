## Description:

Log workouts, plan routines, track progress, and get intelligent coaching for any fitness level.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to plan gym routines, log workouts, track personal records and measurements, adapt training around restrictions, and get general fitness and nutrition guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may keep workout logs, body measurements, weight trends, schedule, goals, and injury restrictions in plaintext files under ~/gym.

Mitigation: Use the skill only if local retention is acceptable, and review or delete those files when needed.

Risk: Injury, supplement, and nutrition guidance may be over-applied as individualized medical advice.

Mitigation: Treat responses as general fitness information and consult a qualified professional for medical, injury-specific, or nutrition-sensitive decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/gym)
- [Workout and routine guidance](artifact/workouts.md)
- [Progress tracking guidance](artifact/progress.md)
- [Injury adaptation guidance](artifact/adaptation.md)
- [Nutrition guidance](artifact/nutrition.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with structured workout, progress, adaptation, nutrition, and local profile/log templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce suggested edits or additions to local plaintext files under ~/gym when the user wants persistent workout tracking.]

## Skill Version(s):

1.0.1 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
