## Description:

Generates printable Chinese activity plans for children ages 3-6 across kindergarten health, language, social, science, and art domains, including goals, materials, steps, parent safety tips, duration, and weekly plan combinations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyumingben](https://clawhub.ai/user/liyumingben)

### License/Terms of Use:

MIT

## Use Case:

External educators, parents, and agents use this skill to select age-appropriate play, craft, experiment, life-task, and weekly-plan activities for kindergarten-aged children. It is intended for activity plans rather than math, thinking, or English worksheet generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad child or activity wording may trigger the skill when the user actually wants worksheets or a different educational task.

Mitigation: Confirm the request is for activity plans, games, crafts, experiments, or family weekly plans before running the generator.

Risk: The generator writes an HTML file to the output path chosen by the user or agent.

Mitigation: Review or set the output path before execution to avoid writing to an unintended location.

Risk: Activities for young children can involve scissors, water, small items, movement, or other supervision-sensitive materials.

Mitigation: Keep the generated parent safety tips visible and require adult review before using an activity with children.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liyumingben/skills/kindergarten-activity-course)
- [ClawHub Homepage Metadata](https://skillhub.cn/skills/user_89a2cacc/kindergarten-activity-course)
- [Activities Reference](references/activities.md)
- [Weekly Plan Template](references/plan-template.md)
- [Related Kindergarten Math Course](https://skillhub.cn/skills/user_89a2cacc/kindergarten-math-course)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese guidance with optional shell commands and generated UTF-8 printable HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script writes a user-directed HTML file containing CSS in a style tag; activity selection can be reproduced with a seed.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
