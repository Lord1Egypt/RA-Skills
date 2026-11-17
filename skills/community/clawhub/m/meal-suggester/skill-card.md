## Description:

Meal Suggester helps an agent provide quick dinner suggestions and maintain local Markdown notes for household preferences, inventory, meal history, and shopping needs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thibautrey](https://clawhub.ai/user/thibautrey)

### License/Terms of Use:


## Use Case:

External users use this skill for local household meal planning, quick dinner suggestions, and shopping-list guidance based on local preference, allergy, inventory, and meal-history notes. Users should review suggestions before cooking, especially when dietary restrictions are recorded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores household preferences, allergies, inventory, meal history, and shopping notes in local Markdown files.

Mitigation: Keep the skill directory private, avoid committing personal household data, and review stored notes before sharing the skill workspace.

Risk: Documented automation may be broader than the shipped script behavior, which mainly picks a random recipe and logs it.

Mitigation: Treat automation claims cautiously and verify inventory matching, learning, shopping-list updates, and reminders in the installed environment before relying on them.

Risk: Meal suggestions can be unsafe or unsuitable if allergy and preference notes are incomplete or out of date.

Mitigation: Keep preference files current and review each suggestion against dietary restrictions before cooking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thibautrey/skills/meal-suggester)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown recipe suggestions with local Markdown note updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only operation; stores household preferences, allergies, inventory, meal history, and shopping notes in Markdown files.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
