## Description:

Meal Planner Pro helps households create personalized weekly meal plans, grocery lists, freezer inventories, prep schedules, and recipe suggestions based on tastes, allergies, dietary restrictions, ratings, and available ingredients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT

## Use Case:

Household users use this skill to plan meals, generate shopping lists, track preferences and freezer inventory, and get recipe ideas from available ingredients or fridge photos. It is intended for recurring personal meal-planning workflows where allergy and preference constraints matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive household details such as names, ages, allergies, dietary restrictions, meal ratings, meal history, freezer inventory, and possibly food photos.

Mitigation: Review the skill before installing, keep generated data in private local or authenticated storage, and avoid sharing household files or photos outside the intended environment.

Risk: First-run setup commands can overwrite existing data files if setup is rerun in a populated skill directory.

Mitigation: Run setup only from the intended skill directory and back up existing data before rerunning setup.

Risk: The artifact includes under-disclosed promotional cross-sells that may introduce unsolicited product mentions.

Mitigation: Remove or disable the Cross-Sells section before deployment if unsolicited product recommendations are not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-meal-planner-pro)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [First-run setup](artifact/SETUP-PROMPT.md)
- [Dietary profiles](artifact/config/dietary-profiles.md)
- [Cuisine categories](artifact/config/cuisine-categories.md)
- [Store sections](artifact/config/store-sections.md)
- [Dashboard specification](artifact/dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON data files, setup shell commands, and structured meal-planning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local household profile, rating, meal-history, freezer, meal-plan, grocery-list, and prep-plan files.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
