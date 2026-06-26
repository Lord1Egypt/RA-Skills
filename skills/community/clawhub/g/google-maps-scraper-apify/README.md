# Google Maps Scraper Skill for OpenClaw and AI Agents

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-green.svg)](./LICENSE)
[![Apify Actor](https://img.shields.io/badge/Apify-kLdarP5qiTvc9CwtP-ff6b00)](https://console.apify.com/actors/kLdarP5qiTvc9CwtP/source)
[![Skill Type](https://img.shields.io/badge/OpenClaw-Skill-111827)](./SKILL.md)
[![skills.sh](https://skills.sh/b/hundevmode/apify-google-maps-scraper-agent-skill)](https://skills.sh/hundevmode/apify-google-maps-scraper-agent-skill)

AI-agent skill for running a production Google Maps Scraper through Apify. It helps agents create correct payloads, control budget, run the actor, and return structured Google Maps business data for lead generation, local SEO, market research, directory building, and CRM enrichment.

Default actor:

- Actor ID: [`kLdarP5qiTvc9CwtP`](https://console.apify.com/actors/kLdarP5qiTvc9CwtP/source)
- Store page: [https://apify.com/x_guru/google-maps-scraper](https://apify.com/x_guru/google-maps-scraper)
- Auth: `APIFY_TOKEN`

## What This Skill Does

- Builds Google Maps scraper payloads from natural-language requests.
- Runs Google Maps place discovery by search term and location.
- Supports direct Google Maps URLs and Google Place IDs.
- Enables optional add-ons: place details, website contacts, reviews, and images.
- Applies Apify run budget guard with `maxTotalChargeUsd`.
- Returns JSON rows that can be used by n8n, Google Sheets, Airtable, CRM systems, or custom pipelines.

## Repository Structure

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Agent trigger rules, payload rules, workflow, and output contract |
| `agents/openai.yaml` | OpenClaw UI metadata |
| `scripts/google_maps_scraper_actor.py` | CLI runner for the Apify actor |
| `references/actor-input-guide.md` | Detailed input field guide |
| `references/sample_input.json` | Ready-to-run sample payload |
| `references/troubleshooting.md` | Common failures and fixes |

## Requirements

- Python 3.10+
- no third-party Python packages required
- Apify API token

Install:

```bash
pip install -r requirements.txt
```

Set token:

```bash
export APIFY_TOKEN='apify_api_xxx'
```

## Quick Start

Run a small Google Maps lead discovery job:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_scraper_actor.py quick-search \
  --query "bike repair shop" \
  --location "Portland, Oregon, USA" \
  --limit 25 \
  --budget-usd 1
```

Run with website contact enrichment:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_scraper_actor.py quick-search \
  --query "roofing contractor" \
  --location "Denver, Colorado, USA" \
  --limit 50 \
  --with-contacts \
  --only-with-website \
  --budget-usd 2
```

Run with Google Maps reviews:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_scraper_actor.py quick-search \
  --query "dentist" \
  --location "Austin, Texas, USA" \
  --limit 20 \
  --reviews 10 \
  --reviews-sort newest \
  --budget-usd 1
```

Run custom JSON:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_scraper_actor.py run \
  --input-file references/sample_input.json \
  --budget-usd 2
```

## Common Agent Use Cases

### Local business lead generation

Use `searchStringsArray`, `locationQuery`, `maxCrawledPlacesPerSearch`, and optionally `scrapeCompanyContacts`.

### Google Maps review collection

Use `maxReviews`, `reviewsSort`, `reviewsStartDate`, `reviewsOrigin`, and `scrapeReviewsPersonalData`.

### CRM enrichment

Use `startUrls` or `placeIds` with `scrapePlaceDetailPage` and optional website contact enrichment.

### Local SEO and competitor research

Use category/rating/website filters and export title, category, address, rating, reviews count, website, phone, Place ID, CID, and coordinates.

## Output Format

The runner prints JSON:

```json
{
  "ok": true,
  "actorId": "kLdarP5qiTvc9CwtP",
  "fetchedAt": "2026-06-01T00:00:00+00:00",
  "itemCount": 25,
  "inputUsed": {
    "searchStringsArray": ["bike repair shop"],
    "locationQuery": "Portland, Oregon, USA",
    "maxCrawledPlacesPerSearch": 25
  },
  "rows": []
}
```

`rows` contains dataset items returned by the Apify actor.

Common row fields include business identity, address, contacts, ratings, reviews, images, opening hours, Google IDs, and nested add-on data. See `references/actor-input-guide.md` for the full grouped output contract.

## Install as OpenClaw Skill

If your OpenClaw or ClawHub runtime supports GitHub install:

```bash
npx skills add hundevmode/apify-google-maps-scraper-agent-skill --skill google-maps-scraper-apify
```

List skills in the repo:

```bash
npx skills add hundevmode/apify-google-maps-scraper-agent-skill --list
```

Install into Codex or another supported agent through the Skills CLI:

```bash
npx skills add hundevmode/apify-google-maps-scraper-agent-skill \
  --skill google-maps-scraper-apify \
  --agent codex \
  -y
```

## Security

- Do not hardcode Apify tokens.
- Prefer `APIFY_TOKEN` environment variable.
- Start with small jobs before scaling.
- Use `--budget-usd` for controlled runs.
- Avoid collecting reviewer personal data unless the user explicitly needs it and the use case allows it.

## SEO Keywords

Google Maps scraper skill, Apify Google Maps actor, Google Maps leads, Google Maps business scraper, local business scraper, Google reviews scraper, Google Maps API workflow, AI agent scraping skill, OpenClaw skill, ClawHub skill, local SEO automation, business contact enrichment.

## License

MIT-0, matching ClawHub skill publishing terms.
