## Description:

Plan meals with weekly menus, shopping lists, batch cooking, budget tracking, dietary preferences, and recipe management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to plan household meals, generate shopping lists, organize recipes, coordinate dietary preferences, track food budget, and reduce food waste. It supports the full meal lifecycle from planning through shopping, prep, cooking, and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meal planning memory may include dietary restrictions, allergies, household details, preferences, and budget information in local plaintext markdown files.

Mitigation: Store only details needed for planning, prefer nicknames or coarse age groups, avoid unnecessary sensitive information, and delete ~/meal-planner/ to remove the stored data.

Risk: Incorrect handling of allergies, intolerances, or health-related dietary needs could lead to unsafe or unsuitable meal suggestions.

Mitigation: Review meal plans against current restrictions, mark severity for each restriction, reject incompatible recipes before use, and consult a qualified professional for medical nutrition needs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/meal-planner)
- [Skill Homepage](https://clawic.com/skills/meal-planner)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown plans, lists, templates, and conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local plaintext markdown files under ~/meal-planner/ when the user engages with meal planning.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
