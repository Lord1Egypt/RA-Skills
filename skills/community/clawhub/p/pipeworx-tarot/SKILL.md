# Tarot

Draw tarot cards, search the deck, and look up meanings. All 78 cards of the Rider-Waite deck are available with upright and reversed interpretations.

## The deck at your fingertips

| Tool | Description |
|------|-------------|
| `random_card` | Draw one card at random |
| `draw_cards` | Draw 1-78 cards (for spreads -- 3-card past/present/future, 10-card Celtic Cross, etc.) |
| `search_cards` | Search by keyword across names and descriptions ("moon", "strength", "cups") |
| `get_card` | Look up a specific card by short name |

## Card naming

Short names follow a pattern: Major Arcana use `ar` prefix (`ar00` = The Fool, `ar01` = The Magician), Minor Arcana use suit + value (`wap01` = Ace of Wands, `cup10` = Ten of Cups, `swkn` = Knight of Swords, `pequ` = Queen of Pentacles).

## Example: draw a 3-card spread

```bash
curl -X POST https://gateway.pipeworx.io/tarot/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"draw_cards","arguments":{"count":3}}}'
```

Each card comes with its name, suit, type (Major/Minor Arcana), upright meaning, reversed meaning, and a description.

```json
{
  "mcpServers": {
    "tarot": {
      "url": "https://gateway.pipeworx.io/tarot/mcp"
    }
  }
}
```
