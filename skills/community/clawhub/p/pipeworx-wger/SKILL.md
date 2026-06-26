# Wger (Workout Manager)

Exercise database with muscle groups, equipment, and detailed exercise descriptions. Useful for building workout routines, fitness apps, or answering "what exercises target my biceps?"

## Tools overview

- `list_exercises` -- Browse exercises (English only). Returns name, description, category, primary and secondary muscles, and equipment needed. Default 20 results.
- `get_exercise` -- Full details for a specific exercise by its numeric ID.
- `list_muscles` -- Every muscle in the database with front/back body position.
- `list_equipment` -- All equipment types: barbell, dumbbell, kettlebell, gym mat, pull-up bar, etc.

## Example: list exercises

```bash
curl -X POST https://gateway.pipeworx.io/wger/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"list_exercises","arguments":{"limit":10}}}'
```

## Building a workout

1. Use `list_muscles` to identify target muscle IDs
2. Browse exercises with `list_exercises`
3. Get full descriptions and equipment needs with `get_exercise`

```json
{
  "mcpServers": {
    "wger": {
      "url": "https://gateway.pipeworx.io/wger/mcp"
    }
  }
}
```
