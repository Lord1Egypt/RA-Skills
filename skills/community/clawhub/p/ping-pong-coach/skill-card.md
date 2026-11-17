## Description:

Generates Chinese-language table-tennis training plans that use a learner's age, optional gender, and years of practice to identify the current stage, estimate remaining learning time, and outline staged technical priorities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taradl7347c](https://clawhub.ai/user/taradl7347c)

### License/Terms of Use:

MIT-0

## Use Case:

External users and coaching assistants use this skill to create Chinese-language table-tennis lesson plans for learners aged 5-60 based on age, optional gender, and training history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may trigger broadly on table-tennis lesson-plan requests.

Mitigation: Confirm the user wants a table-tennis training plan and collect age, training years, and optional gender before generating the plan.

Risk: The local script only computes stage and progress, so script output alone is not a complete training plan.

Mitigation: Use the bundled curriculum reference for stage details and present the script output as stage analysis within the broader plan.

## Reference(s):

- [Table-Tennis Curriculum Reference](references/curriculum.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown training plan with stage analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include missing-information notes and next-step coaching recommendations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
