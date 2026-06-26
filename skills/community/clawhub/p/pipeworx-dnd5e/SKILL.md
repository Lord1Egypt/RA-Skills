---
name: pipeworx-dnd5e
description: D&D 5th Edition reference — spells, monsters, classes, and spell lists from the official SRD
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🐉"
    homepage: https://pipeworx.io/packs/dnd5e
---

# D&D 5th Edition

The complete D&D 5e Systems Reference Document at your fingertips. Look up spells, monsters, and character classes from the official SRD. Perfect for game night prep, character building, or settling rules disputes.

## Tools

| Tool | Description |
|------|-------------|
| `get_spell` | Full spell details by index name in kebab-case (e.g., "fireball", "magic-missile") |
| `get_monster` | Monster stat block including HP, AC, abilities, and actions (e.g., "goblin", "dragon-red-adult") |
| `get_class` | Class features, proficiencies, and hit dice (e.g., "wizard", "fighter", "cleric") |
| `list_spells` | All available spells with their index names |

## Perfect for

- "What does the Fireball spell do?" — instant lookup during a game session
- Checking a monster's CR, hit points, and special abilities before an encounter
- Reviewing class features when creating a new character
- Building a D&D companion app with searchable SRD content

## Example: look up Fireball

```bash
curl -s -X POST https://gateway.pipeworx.io/dnd5e/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_spell","arguments":{"index":"fireball"}}}'
```

Returns: name, level, school, casting time, range, components, duration, description, damage at each level, and available classes.

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-dnd5e": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/dnd5e/mcp"]
    }
  }
}
```

## Tip

Spell and monster index names use kebab-case. If you're unsure of the exact name, use `list_spells` first to browse available options.
