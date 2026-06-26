---
name: pipeworx-dadjokes
description: The finest dad jokes on the internet — random, searchable, and groan-worthy from icanhazdadjoke.com
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "😄"
    homepage: https://pipeworx.io/packs/dadjokes
---

# Dad Jokes

Why did the scarecrow win an award? Because he was outstanding in his field. This pack serves up dad jokes from icanhazdadjoke.com — the internet's premier repository of wholesome, groan-inducing humor.

## Tools

- **`random_joke`** — A random dad joke, ready to deploy
- **`search_jokes`** — Search the collection by keyword (e.g., "cat", "pizza", "coffee")
- **`get_joke`** — Fetch a specific joke by its ID

## Ideal for

- Lightening the mood in a conversation
- "Tell me a joke" requests in chatbots
- Slack/Discord bots that post daily jokes
- Teaching moments about search and APIs (everyone loves a good dad joke)

## Example

```bash
curl -s -X POST https://gateway.pipeworx.io/dadjokes/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_jokes","arguments":{"term":"coffee","limit":3}}}'
```

```json
{
  "results": [
    { "id": "71wsPKeF6h", "joke": "I just got my doctor's test results and I'm really upset. Turns out, I'm not a doctor." }
  ],
  "total_jokes": 1
}
```

## Setup

```json
{
  "mcpServers": {
    "pipeworx-dadjokes": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/dadjokes/mcp"]
    }
  }
}
```
