## Description:

AI weight-loss companion that uses yesterday's diet calories to calculate today's step goal, supervise step completion, and support food, weight, schedule, menstrual-cycle, and binge-recovery check-ins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyoung310](https://clawhub.ai/user/joeyoung310)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this Chinese-language skill as a weight-loss coaching companion that records diet and steps, estimates calorie intake, sets daily step goals from prior-day intake, and generates progress feedback. It should be treated as non-medical wellness support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores health-related profile, diet, step, and conversation data locally.

Mitigation: Install only when local storage of this sensitive wellness data is acceptable, and restrict access to the data directory.

Risk: Supplement, fasting, menstrual-cycle, and binge-recovery guidance is medical-adjacent.

Mitigation: Present it as non-medical coaching and direct users to a clinician for medical decisions or concerning symptoms.

Risk: The data manager has a record-path validation issue when handling dates for local JSON records.

Mitigation: Validate date inputs before automated writes or use with untrusted dates.

## Reference(s):

- [Common food calorie reference](references/food_calories.md)
- [ClawHub skill page](https://clawhub.ai/joeyoung310/skills/kite-slim)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured text, with optional JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include calorie estimates, step goals, daily check-in summaries, profile or record updates, and non-medical coaching guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
