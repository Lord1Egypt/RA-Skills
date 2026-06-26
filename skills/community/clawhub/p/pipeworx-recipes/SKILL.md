# Recipes

What should I cook tonight? Search thousands of recipes, look up full ingredient lists and instructions, or let the API surprise you with a random meal.

## What's on the menu

- **search_meals** -- Search recipes by name ("pasta", "chicken tikka")
- **get_meal** -- Full recipe by ID: ingredients with measurements, step-by-step instructions, video link
- **random_meal** -- Feeling lucky? Get a random recipe
- **meals_by_ingredient** -- Got chicken in the fridge? Find every recipe that uses it

## Example: search for pasta recipes

```bash
curl -X POST https://gateway.pipeworx.io/recipes/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_meals","arguments":{"query":"carbonara"}}}'
```

## What a full recipe looks like

Each recipe includes the meal name, category (Beef, Dessert, Seafood...), cuisine area (Italian, Japanese, Mexican...), full instructions, up to 20 ingredients with measurements, thumbnail image, YouTube tutorial link, and source URL.

## Integration

```json
{
  "mcpServers": {
    "recipes": {
      "url": "https://gateway.pipeworx.io/recipes/mcp"
    }
  }
}
```

Data from TheMealDB.
