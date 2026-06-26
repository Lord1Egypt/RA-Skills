---
name: mealmastery
description: Plan meals, manage recipes, and build grocery lists with AI through natural language conversation.
version: 1.0.1
homepage: https://www.mealmastery.ai
changelog: "v1.0.1: Fix GitHub repository URL to point to public repo (MealMasteryAI/mcp-server). No functional changes."
metadata:
  openclaw:
    emoji: "🍽️"
    primaryEnv: MEALMASTERY_API_KEY
    os:
      - darwin
      - linux
      - win32
    requires:
      env:
        - MEALMASTERY_API_KEY
      bins:
        - node
    install:
      - kind: node
        package: "@mealmastery/mcp-server"
---

# MealMastery

AI-powered meal planning, recipe management, and grocery list generation. Generate a personalized weekly meal plan, save your favorites, build a consolidated grocery list, and send it to Instacart or Kroger -- all through conversation.

## Setup

1. Create a free account at [mealmastery.ai](https://www.mealmastery.ai)
2. Go to **Settings > Developer API** and create an API key
3. Set the key in your environment:

```sh
export MEALMASTERY_API_KEY="mm_live_..."
```

MCP server configuration (`~/.openclaw/config.json`):

```json
{
  "mcpServers": {
    "mealmastery": {
      "command": "npx",
      "args": ["-y", "@mealmastery/mcp-server"],
      "env": {
        "MEALMASTERY_API_KEY": "${MEALMASTERY_API_KEY}"
      }
    }
  }
}
```

Verify the connection works by asking: *"What are my meal planning preferences?"*

## Tools (24)

### Meal Planning (7 tools)
`generate_meal_plan` `get_latest_meal_plan` `get_meal_plan` `list_meal_plans` `regenerate_meal` `generate_and_add_meal` `remove_meal`

### Recipes (7 tools)
`search_recipes` `get_recipe` `save_meal_as_recipe` `get_favorite_recipes` `favorite_meal` `get_meal_ratings` `get_all_ratings`

### Grocery Lists (4 tools)
`generate_grocery_list` `get_grocery_list` `list_grocery_lists` `update_grocery_items`

### User & Checkout (6 tools)
`get_user_context` `get_user_preferences` `update_user_preferences` `get_subscription_status` `get_checkout_providers` `checkout_grocery_list`

## Resources (3)

Read-only context that agents can fetch without using a tool call.

| URI | Description |
|---|---|
| `mealmastery://meal-plan/current` | Latest meal plan with all meals, nutrition, and recipes |
| `mealmastery://user/preferences` | Dietary preferences, allergies, cooking skill, favorites |
| `mealmastery://grocery-list/current` | Grocery list for the current meal plan |

## Prompt Templates (4)

Pre-built workflow starters for common multi-step tasks.

| Prompt | Parameters | Description |
|---|---|---|
| `weekly-meal-prep` | `focus?`, `days?` | Full week planning: preferences, generate, review, grocery list, checkout |
| `swap-meal` | `reason?` | Replace a specific meal in the current plan |
| `order-groceries` | `provider?` | Preview and send grocery list to Instacart or Kroger |
| `quick-dinner` | `max_minutes?`, `ingredients?` | Single quick meal idea with time/ingredient constraints |

## Streaming

`generate_meal_plan` supports MCP progress notifications. Clients that send a `progressToken` receive real-time updates (0-100%) during AI generation via the SSE streaming endpoint. Clients without progress support fall back to the standard blocking endpoint.

## Example Workflows

**Weekly meal prep:**
> "Generate a healthy meal plan for 2 people, Mediterranean style, max 30 minutes prep. Then create the grocery list."

Uses: `get_user_context` -> `generate_meal_plan` -> `generate_grocery_list`

**Swap a meal:**
> "Replace Wednesday's dinner with something Thai."

Uses: `get_latest_meal_plan` -> `regenerate_meal`

**Order groceries:**
> "Send my grocery list to Instacart."

Uses: `checkout_grocery_list` (dry_run=true first, then with confirmation)

## Guardrails

- **Checkout safety.** Always call `checkout_grocery_list` with `dry_run=true` first and show the preview. Only execute the real checkout after explicit user confirmation. This adds items to a real shopping cart.
- **Preference changes.** Confirm with the user before calling `update_user_preferences` for dietary restrictions or allergies. These affect all future meal plans.
- **Destructive operations.** `remove_meal` permanently deletes a meal from a plan. Confirm before calling.
- **Rate limits.** Meal plan generation counts against the user's subscription quota. Check `get_subscription_status` if the user is on a free tier before generating.
- **AI generation time.** `generate_meal_plan` takes 30-60 seconds. `regenerate_meal` and `generate_and_add_meal` take 15-30 seconds. Inform the user these operations are running.
- **Daily quotas.** Free tier: 1,000 requests/day. Paid tier: 10,000 requests/day. Quota info is available after token exchange.

## Publisher

**MealMastery Inc.** -- [mealmastery.ai](https://www.mealmastery.ai) | [GitHub](https://github.com/MealMasteryAI/mcp-server) | [Support](mailto:b.moore@mealmastery.ai)
