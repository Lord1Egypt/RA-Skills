# Superhero

A database of 731 superheroes and villains with power stats, biographies, and images. Covers Marvel, DC, and more.

## Available tools

**list_all** returns every hero with their ID, name, and slug. Use this to browse or find IDs.

**get_hero** returns the complete profile for a hero by ID: powerstats (intelligence, strength, speed, durability, power, combat), appearance (gender, race, height, weight, eye color, hair color), biography (full name, aliases, publisher, first appearance, alignment), work, connections, and images.

**get_powerstats** returns just the six power statistics for quick comparisons.

**get_biography** returns biographical details: full name, alter egos, aliases, place of birth, first appearance, publisher, and alignment (good/bad/neutral).

## Example: compare Batman and Superman

```bash
curl -X POST https://gateway.pipeworx.io/superhero/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_powerstats","arguments":{"id":70}}}'
```

Batman is ID 70. Superman is ID 644. Spider-Man is ID 620. Wonder Woman is ID 720.

```json
{
  "mcpServers": {
    "superhero": {
      "url": "https://gateway.pipeworx.io/superhero/mcp"
    }
  }
}
```
