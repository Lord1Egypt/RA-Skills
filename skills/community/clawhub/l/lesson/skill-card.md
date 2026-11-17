## Description:

Generates Chinese-language daily menu recommendations from available ingredients, taste preferences, party size, and cooking time, using bundled ingredient and recipe references to produce menus and step-by-step cooking guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yequanzheng](https://clawhub.ai/user/yequanzheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill as a Chinese-language meal planner to choose dishes from ingredients they already have, account for preferences and time limits, and receive a practical menu, prep list, cooking steps, and timeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cooking recommendations may be incomplete or unsuitable for a user's allergy, food-safety, dietary, or equipment constraints.

Mitigation: Ask users to state allergies and restrictions, and review meal plans before cooking, especially for raw or high-risk ingredients.

Risk: The helper script can overwrite a file when a user explicitly supplies an output path.

Mitigation: Use stdout by default or choose a deliberate non-sensitive output path before running the script with --output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yequanzheng/skills/lesson)
- [Ingredient database](references/ingredients.md)
- [Recipe database](references/recipes.md)
- [Evaluation prompts](evals/evals.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown menu guidance for agent responses; optional JSON from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include dish recommendations, ingredient prep lists, cooking steps, estimated timing, calorie notes for lighter styles, and follow-up suggestions.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
