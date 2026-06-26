## Description: <br>
Generates personalized daily menu recommendations from available ingredients, taste preferences, diner count, and cooking time, using bundled ingredient and recipe references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yequanzheng](https://clawhub.ai/user/yequanzheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to turn available foods and preferences into practical meal plans, prep lists, cooking steps, and cooking timelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Food and menu prompts can include dietary restrictions, allergies, or sensitive health details. <br>
Mitigation: Ask only for details needed for meal planning and avoid collecting unnecessary sensitive personal health information. <br>
Risk: Cooking guidance may be unsuitable when users have allergies, medical diets, or food-safety constraints. <br>
Mitigation: Encourage users to state allergies or restrictions and review recipe suitability before cooking. <br>


## Reference(s): <br>
- [Ingredient Database](references/ingredients.md) <br>
- [Recipe Database](references/recipes.md) <br>
- [Evaluation Scenarios](evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown meal plan with menu recommendations, ingredient prep tables, step-by-step cooking guidance, and timeline suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bundled ingredient and recipe data and user-provided meal preferences; no hidden access, persistence, or unsafe behavior was identified in security evidence.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
