## Description:

Guides personalized workout planning, exercise instruction, training analysis, progression, and nutrition using an exercise database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiji-z](https://clawhub.ai/user/kaiji-z)

### License/Terms of Use:

MIT-0

## Use Case:

People seeking fitness guidance use this skill to build or adjust training plans, learn exercises, interpret workout reports, and get nutrition and progression advice. It can produce plans for Workout Timer App import.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database setup and updates retrieve exercise data from Gitee without pinned integrity checks.

Mitigation: Run setup or updates only when you trust the data source.

Risk: Injury, body, and diet details can be sensitive if stored in the agent environment.

Mitigation: Avoid persisting those details unless comfortable with the environment's data handling.

Risk: Fitness plans may be unsuitable for a person's injuries or limitations.

Mitigation: Review plans against individual goals, equipment, and injuries; prioritize safe movement and conservative adjustments.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/kaiji-z/skills/kaiji-fitness-coach)
- [Free Exercise DB](https://gitee.com/kaiji1126/free-exercise-db)
- [Exercise database schema](references/exercise-db-schema.md)
- [Workout Timer App integration](references/workout-timer-integration.md)

## Skill Output:

**Output Type(s):** [Fitness guidance, Training plans, Workout analysis, JSON configuration]

**Output Format:** [Markdown tables and prose, or plain JSON for app import]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [App plans use standard English exercise names from the database.]

## Skill Version(s):

2.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
