## Description: <br>
Meal Planner Pro helps an agent create personalized household meal plans, grocery lists, prep schedules, freezer tracking, and fridge-photo recipe suggestions based on dietary needs and preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Household users use this skill to plan weekly meals, maintain household dietary profiles, generate organized grocery lists, and adapt plans from ratings, freezer inventory, schedules, and visible fridge or pantry ingredients. It is intended for personal meal-planning workflows where allergy and preference data must remain private and user-verified. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores household names, ages, allergy details, preferences, meal ratings, freezer contents, and possible food-photo context. <br>
Mitigation: Keep the local data directory private, minimize unnecessary identifying details for children, and use the optional dashboard only with proper authentication, row-level security, private storage, and proxied external images. <br>
Risk: Meal suggestions that involve allergies or dietary constraints can be incomplete or wrong. <br>
Mitigation: Have the user independently verify allergy-sensitive meal suggestions, ingredients, labels, and cross-contamination risks before preparing or serving food. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nollio/normieclaw-meal-planner-pro) <br>
- [Publisher profile](https://clawhub.ai/user/nollio) <br>
- [Dietary Profiles](config/dietary-profiles.md) <br>
- [Cuisine Categories](config/cuisine-categories.md) <br>
- [Store Sections](config/store-sections.md) <br>
- [Dashboard Specification](dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Conversational meal-planning guidance, markdown grocery and prep lists, and local JSON data files for household profiles, ratings, meal plans, grocery lists, and freezer inventory.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a vision-capable model for fridge-photo mode and may be paired with an optional authenticated dashboard.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
