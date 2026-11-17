## Description:

Plan meals, manage recipes, and build grocery lists with AI through natural language conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rooster-cogburn77](https://clawhub.ai/user/rooster-cogburn77)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to MealMastery for weekly meal planning, recipe lookup and saving, grocery-list generation, and checkout preparation through natural language workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm MCP server locally with the user's MealMastery API key.

Mitigation: Use a pinned and reviewed package version or a sandboxed/containerized MCP runtime, and prefer a revocable scoped API key when available.

Risk: Checkout workflows can add groceries to a real Instacart or Kroger shopping cart.

Mitigation: Run checkout in dry-run mode first, show the preview, and proceed only after explicit user confirmation.

Risk: Preference or allergy updates affect future meal plans and recommendations.

Mitigation: Confirm dietary restriction, allergy, and preference changes with the user before calling update tools.

Risk: Meal deletion permanently removes a meal from a plan.

Mitigation: Confirm destructive meal-removal requests before calling remove_meal.

## Reference(s):

- [MealMastery website](https://www.mealmastery.ai)
- [MealMastery MCP server repository](https://github.com/MealMasteryAI/mcp-server)
- [ClawHub skill listing](https://clawhub.ai/rooster-cogburn77/skills/mealmastery)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Conversational text and structured MCP tool results, often rendered as Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEALMASTERY_API_KEY and a local Node-based MCP server; checkout actions should be previewed before confirmation.]

## Skill Version(s):

1.0.1 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
