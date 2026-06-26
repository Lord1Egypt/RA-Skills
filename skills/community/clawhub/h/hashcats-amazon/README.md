# HashCats Amazon Intelligence — OpenClaw Skill

This is the official OpenClaw/ClawHub skill for the **HashCats API** (`https://api.hashcats.io`).

It teaches OpenClaw agents how to use the x402-native Amazon product intelligence endpoints without any API keys — agents pay tiny USDC amounts automatically on 402 responses.

## What's Included

- Full natural language Amazon search
- Filtering, ranking, and deep product details extraction
- One-shot `/best` workflow (search + filter + rank in one call)

## Skill Files

- `SKILL.md` — Main instructions read by the agent
- `examples/` — Request + response examples for every endpoint
- `CHANGELOG.md` — Version history

## How to Use

After installing the skill (and the official x402 skill), your agent can say things like:
- "Find the best noise cancelling headphones under $200 that ship fast using HashCats"
- "Get full structured details for https://www.amazon.com/dp/B0GLNV4LJ9"
- "Search Amazon for wireless earbuds, filter, rank by best_value, then show details on the top 2"

## Pricing (micropayments in USDC)
- /search, /filter, /rank → ~$0.003
- /product-details → ~$0.010
- /best (one-shot) → ~$0.020

## Links
- Live API: https://api.hashcats.io
- Docs: https://api.hashcats.io/docs
- OpenAPI: https://api.hashcats.io/openapi.json

Made for the agentic shopping economy. Contributions and feedback welcome!