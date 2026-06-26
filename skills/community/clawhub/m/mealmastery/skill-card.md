## Description: <br>
Plan meals, manage recipes, and build grocery lists with AI through natural language conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rooster-Cogburn77](https://clawhub.ai/user/Rooster-Cogburn77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and meal-planning assistants use this skill to generate meal plans, manage recipes, maintain grocery lists, and preview grocery checkout flows through MealMastery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a MealMastery API key. <br>
Mitigation: Use a dedicated API key where possible and keep MEALMASTERY_API_KEY out of shared logs, prompts, and committed configuration. <br>
Risk: Checkout actions can add groceries to a real shopping cart. <br>
Mitigation: Run checkout_grocery_list with dry_run=true first, show the preview, and execute only after explicit user confirmation. <br>
Risk: Preference updates can affect future meal plans, including allergy and dietary settings. <br>
Mitigation: Confirm allergy, dietary preference, and other profile changes with the user before calling update_user_preferences. <br>
Risk: Meal deletion changes meal plan data. <br>
Mitigation: Confirm the target meal and user intent before calling remove_meal. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Rooster-Cogburn77/mealmastery) <br>
- [MealMastery Homepage](https://www.mealmastery.ai) <br>
- [MealMastery MCP Server npm Package](https://www.npmjs.com/package/@mealmastery/mcp-server) <br>
- [MealMastery MCP Server Repository](https://github.com/MealMasteryAI/mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Natural-language responses, MCP tool calls, and JSON MCP server configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEALMASTERY_API_KEY and node; supports macOS, Linux, and Windows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
