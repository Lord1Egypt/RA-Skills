# Mealie Recipe Import

Add a recipe to a self-hosted [Mealie](https://mealie.io) instance from a **photo**, **plain text**, or a **URL** — with AI-based ingredient parsing, automatic food/unit creation, recipe metadata, and cover-image upload.

Built for the Mealie **v1 API** (app v3.x). Verified against v3.21.0.

## What it does

- Turns a cookbook photo, pasted text, or a recipe URL into a fully structured Mealie recipe
- AI ingredient parsing via Mealie's configured OpenAI/Gemini parser, with an `nlp`/`brute` fallback
- Deduplicates and creates foods & units so you don't end up with duplicates
- Sets servings, yield, times, and step-by-step instructions
- Uploads a cover image (use the finished-dish photo, not the page scan)
- Verifies the result before reporting done

## Requirements

- A running self-hosted Mealie instance (v1 API / app v3.x) reachable over the network
- A Mealie API token
- Python 3 (standard library only — no `pip install`)
- For photo import: an agent with a vision/image capability. Plain-text and URL import work without vision.
- Optional but recommended: an AI ingredient parser configured in Mealie admin (OpenAI or Gemini)

## Setup

Set two environment variables:

- `MEALIE_URL` — e.g. `http://mealie.example.lan:9925`
- `MEALIE_API_KEY` — a long-lived Mealie API token (Mealie UI -> profile -> "Manage Your API Tokens")

Then point your agent at the recipe (photo, text, or URL) and ask it to add it to Mealie.

See `SKILL.md` for the full agent workflow and `scripts/mealie_import.py` for the deterministic helper script (takes a JSON job file).

## Files

- `SKILL.md` — the agent-facing workflow and API reference
- `scripts/mealie_import.py` — stdlib-only Python helper: creates the recipe, dedups/creates foods & units, sets ingredients + steps + metadata, uploads the cover image, and verifies

## License

MIT
