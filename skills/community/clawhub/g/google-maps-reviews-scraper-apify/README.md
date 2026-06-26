# Google Maps Reviews Scraper Skill for OpenClaw and AI Agents

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-green.svg)](./LICENSE)
[![Apify Actor](https://img.shields.io/badge/Apify-V2kIsQs3Ta9C9kkEt-ff6b00)](https://console.apify.com/actors/V2kIsQs3Ta9C9kkEt/source)
[![Skill Type](https://img.shields.io/badge/OpenClaw-Skill-111827)](./SKILL.md)
[![skills.sh](https://skills.sh/b/hundevmode/apify-google-maps-reviews-scraper-agent-skill)](https://skills.sh/hundevmode/apify-google-maps-reviews-scraper-agent-skill)

AI-agent skill for running the Google Maps Reviews Scraper through Apify. It helps agents build correct exact-place review payloads, control spend, run the actor, and return structured Google review rows for local SEO, reputation monitoring, sentiment analysis, BI exports, and competitor research.

Default actor:

- Actor ID: [`V2kIsQs3Ta9C9kkEt`](https://console.apify.com/actors/V2kIsQs3Ta9C9kkEt/source)
- Store page: [https://apify.com/x_guru/google-maps-reviews-scraper](https://apify.com/x_guru/google-maps-reviews-scraper)
- Auth: `APIFY_TOKEN`

## What This Skill Does

- Builds Google Maps reviews scraper payloads from natural-language requests.
- Runs review extraction for exact Google Maps place URLs, CID URLs, review URLs, and Place IDs.
- Supports review count, sort order, date filtering, language, origin, and personal data toggle.
- Applies Apify run budget guard with `maxTotalChargeUsd`.
- Returns rows ready for n8n, Sheets, Airtable, BI, CRM, databases, or custom pipelines.

## Repository Structure

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Agent trigger rules, workflow, payload rules, and output contract |
| `agents/openai.yaml` | OpenClaw UI metadata |
| `scripts/google_maps_reviews_scraper_actor.py` | CLI runner for the Apify actor |
| `references/input-output-contract.md` | Detailed input and output contract |
| `references/sample_input.json` | Ready-to-run sample input |
| `references/troubleshooting.md` | Common failures and fixes |

## Quick Start

Set token:

```bash
export APIFY_TOKEN='apify_api_xxx'
```

Run by Place ID:

```bash
python3 scripts/google_maps_reviews_scraper_actor.py quick-place-id \
  --place-id "ChIJ8Q2WSpJZwokRQz-bYYgEskM" \
  --max-reviews 25 \
  --budget-usd 1
```

Run by URL:

```bash
python3 scripts/google_maps_reviews_scraper_actor.py quick-url \
  --url "https://www.google.com/maps/place/Joe%27s+Pizza/..." \
  --max-reviews 100 \
  --reviews-sort newest \
  --budget-usd 1
```

Run custom JSON:

```bash
python3 scripts/google_maps_reviews_scraper_actor.py run \
  --input-file references/sample_input.json \
  --budget-usd 1
```

## Install as a Skill

OpenClaw or ClawHub:

```bash
npx skills add hundevmode/apify-google-maps-reviews-scraper-agent-skill \
  --skill google-maps-reviews-scraper-apify
```

Codex or another supported Skills CLI agent:

```bash
npx skills add hundevmode/apify-google-maps-reviews-scraper-agent-skill \
  --skill google-maps-reviews-scraper-apify \
  --agent codex \
  -y
```

List skills:

```bash
npx skills add hundevmode/apify-google-maps-reviews-scraper-agent-skill --list
```

## Output

The runner prints JSON with:

- `ok`
- `actorId`
- `fetchedAt`
- `inputUsed`
- `itemCount`
- `rows[]`

Each row is one Google Maps review with review fields, reviewer fields, owner response fields, and place metadata.

## Security

- Do not hardcode Apify tokens.
- Prefer `APIFY_TOKEN` from the environment.
- Use `--budget-usd` for controlled runs.
- Set `personalData=false` when reviewer profile fields are not needed.

## SEO Keywords

Google Maps reviews scraper skill, Google reviews scraper, Apify Google reviews actor, Google review export, Google Place ID reviews, review sentiment workflow, reputation monitoring automation, local SEO reviews, AI agent scraping skill, OpenClaw skill, ClawHub skill.

## License

MIT-0, matching ClawHub skill publishing terms.
