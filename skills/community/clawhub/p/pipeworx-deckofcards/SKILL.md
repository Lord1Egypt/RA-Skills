---
name: pipeworx-deckofcards
description: Virtual card deck — shuffle, draw, and manage playing cards via the Deck of Cards API
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🃏"
    homepage: https://pipeworx.io/packs/deckofcards
---

# Deck of Cards

A virtual deck of playing cards. Create and shuffle decks, draw cards, and reshuffle — all tracked server-side with a persistent deck ID. Supports combining multiple 52-card decks for games like Blackjack.

## Tools

| Tool | Description |
|------|-------------|
| `new_deck` | Create and shuffle a new deck (optionally combine multiple decks). Returns a `deck_id` |
| `draw_cards` | Draw one or more cards from an existing deck. Returns card code, suit, value, and image URL |
| `shuffle_deck` | Reshuffle an existing deck, returning all drawn cards back |

## Useful for

- Simulating card games (poker, blackjack, war)
- Building a card-based decision-making tool
- Teaching probability concepts with real card draws
- Party games where you need a shared virtual deck

## Example: draw a poker hand

```bash
# Step 1: Create a deck
curl -s -X POST https://gateway.pipeworx.io/deckofcards/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"new_deck","arguments":{"count":1}}}'

# Step 2: Draw 5 cards (use the deck_id from step 1)
curl -s -X POST https://gateway.pipeworx.io/deckofcards/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"draw_cards","arguments":{"deck_id":"3p40paa87x90","count":5}}}'
```

Each card includes: code (e.g., "AS" for Ace of Spades), value, suit, and an image URL of the card face.

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-deckofcards": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/deckofcards/mcp"]
    }
  }
}
```
