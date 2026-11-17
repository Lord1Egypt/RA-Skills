## Description:

Personal nutrition and meal planning system with calorie tracking and recipe recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create nutrition profiles, generate meal plans, estimate calories and macronutrients, query food nutrition data, and prepare shopping lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store health-adjacent profile details such as allergies, weight, goals, and dietary restrictions in a local SQLite database.

Mitigation: Use it only on a trusted device and delete ~/.openclaw/data/nutrition-planner/ when the stored nutrition profile is no longer needed.

Risk: The artifact does not include the documented nutrition-planner executable, so the described CLI may not run from this package as released.

Mitigation: Confirm the executable is present before deployment or request a corrected package from the publisher.

## Reference(s):

- [Nutrition Planner ClawHub page](https://clawhub.ai/harrylabsj/skills/nutrition-planner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or reference a local SQLite database under ~/.openclaw/data/nutrition-planner/ when the documented CLI is available.]

## Skill Version(s):

1.0.1 (source: evidence release, SKILL.md frontmatter, SKILL_EN.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
