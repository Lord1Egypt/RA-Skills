## Description:

Fitness accountability for the Lofy AI assistant -- workout logging from natural language, meal tracking with calorie/protein estimates, PR detection with Epley formula, gym reminders based on weekly targets, and progress reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrey401](https://clawhub.ai/user/harrey401)

### License/Terms of Use:


## Use Case:

External users use this skill with the Lofy AI assistant to log workouts and meals, track personal records, manage weekly gym consistency, and generate concise fitness progress summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain sensitive local health, workout, meal, weight-goal, and personal-record history in data/fitness.json.

Mitigation: Use it only for explicit fitness logging requests and review or delete data/fitness.json when that retained history is no longer wanted.

Risk: The release security verdict is suspicious because sensitive health and meal data can be stored without clear consent or retention controls.

Mitigation: Confirm user consent before logging personal fitness or meal information and keep responses focused on rest when injury or pain is mentioned.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown and JSON-oriented guidance for updating local fitness records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local data/fitness.json records for workouts, meals, goals, personal records, and weekly summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
