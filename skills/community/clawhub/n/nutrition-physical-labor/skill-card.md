## Description:

Nutrition and hydration guidance for physically demanding occupations, including construction, trades, agriculture, food service, warehousing, and other jobs requiring sustained physical effort.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to provide practical meal timing, calorie, hydration, electrolyte, recovery, and budget meal-prep guidance for people doing physically demanding work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad filesystem access that is not needed for ordinary nutrition guidance.

Mitigation: Remove or narrow filesystem access unless a specific workflow requires it.

Risk: The install command uses a mutable npx package reference.

Mitigation: Prefer a pinned or integrity-verified install and review the package before deployment.

Risk: Weather and meal-prep reminder behavior can affect users if enabled unexpectedly.

Mitigation: Enable reminders only after explicit user choice and keep them easy to disable.

## Reference(s):

- [Nutrition Physical Labor on ClawHub](https://clawhub.ai/howtousehumans/skills/nutrition-physical-labor)
- [howtousehumans Publisher Profile](https://clawhub.ai/user/howtousehumans)
- [American College of Sports Medicine](https://www.acsm.org)
- [NIOSH Heat Stress Recommendations](https://www.cdc.gov/niosh/topics/heatstress/)
- [USDA Dietary Guidelines for Americans](https://www.dietaryguidelines.gov)
- [Sports Dietitians Australia](https://www.sportsdietitians.com.au)
- [Anthropic Labor Market Impacts of AI](https://www.anthropic.com/research/labor-market-impacts)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with structured meal, hydration, and recovery recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May tailor recommendations by job type, body weight, climate, budget, current eating pattern, and regional food availability.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
