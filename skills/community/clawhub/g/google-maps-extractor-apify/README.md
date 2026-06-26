# Google Maps Extractor Skill for OpenClaw and AI Agents

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-green.svg)](./LICENSE)
[![Apify Actor](https://img.shields.io/badge/Apify-2A4RTA5PjN7McqJXx-ff6b00)](https://console.apify.com/actors/2A4RTA5PjN7McqJXx/source)
[![Skill Type](https://img.shields.io/badge/OpenClaw-Skill-111827)](./SKILL.md)
[![skills.sh](https://skills.sh/b/hundevmode/apify-google-maps-extractor-agent-skill)](https://skills.sh/hundevmode/apify-google-maps-extractor-agent-skill)

AI-agent skill for running a production Google Maps Extractor through Apify. It helps agents create correct payloads, control budget, run the actor, and return structured Google Maps place and business data for local lead generation, local SEO, competitor research, directory building, store locator datasets, and CRM enrichment.

![Real Google Maps search results for bike repair shops in Portland](https://api.apify.com/v2/key-value-stores/RgWfy9bTkPpSqNzrV/records/google-maps-extractor-real-google-maps.png?signature=1c5HpULMOkoXKSytZxW0G)

Default actor:

- Actor ID: [`2A4RTA5PjN7McqJXx`](https://console.apify.com/actors/2A4RTA5PjN7McqJXx/source)
- Store page: [https://apify.com/x_guru/google-maps-extractor](https://apify.com/x_guru/google-maps-extractor)
- Auth: `APIFY_TOKEN`

## What This Skill Does

- Builds Google Maps Extractor payloads from natural-language requests.
- Runs Google Maps place discovery by search term and location.
- Supports direct Google Maps URLs and Google Place IDs.
- Supports category, rating, website, matching, and closed-place filters.
- Enables optional add-ons for place details and public website contacts.
- Applies Apify run budget guard with `maxTotalChargeUsd`.
- Returns JSON rows that can be used by n8n, Google Sheets, Airtable, CRM systems, BI tools, databases, or custom pipelines.

## Repository Structure

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Agent trigger rules, payload rules, workflow, and output contract |
| `agents/openai.yaml` | OpenClaw UI metadata |
| `scripts/google_maps_extractor_actor.py` | CLI runner for the Apify actor |
| `references/input-output-contract.md` | Detailed input and output contract |
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

Run a small Google Maps extraction job:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_extractor_actor.py quick-search \
  --query "bike repair shop" \
  --location "Portland, Oregon, USA" \
  --limit 25 \
  --budget-usd 1
```

Run with public website contact enrichment:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_extractor_actor.py quick-search \
  --query "roofing contractor" \
  --location "Denver, Colorado, USA" \
  --limit 50 \
  --with-contacts \
  --only-with-website \
  --budget-usd 2
```

Run by Google Maps URL:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_extractor_actor.py quick-url \
  --url "https://www.google.com/maps/search/restaurants+near+New+York,+NY" \
  --limit 50 \
  --budget-usd 1
```

Run by Google Place ID:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_extractor_actor.py quick-place-id \
  --place-id "ChIJN1t_tDeuEmsRUsoyG83frY4" \
  --details \
  --budget-usd 1
```

Run custom JSON:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/google_maps_extractor_actor.py run \
  --input-file references/sample_input.json \
  --budget-usd 1
```

## Common Agent Use Cases

### Local business lead generation

Use `searchStringsArray`, `locationQuery`, `maxCrawledPlacesPerSearch`, `website: "withWebsite"`, and `scrapeContacts`.

### Google Maps business data export

Use the core fields only when the user needs names, categories, addresses, phone numbers, websites, ratings, review counts, coordinates, Place IDs, CIDs, and Google Maps URLs.

### CRM enrichment

Use `startUrls` or `placeIds` with `scrapePlaceDetailPage` and optional `scrapeContacts`.

### Local SEO and competitor research

Use category/rating/website filters and export title, category, address, rating, reviews count, website, phone, Place ID, CID, coordinates, and opening status.

### Store locator datasets

Use concrete city, postal code, state, county, or custom map area inputs and export addresses, coordinates, opening hours, Google Maps URLs, and identifiers.

## Output Format

The runner prints JSON:

```json
{
  "ok": true,
  "actorId": "2A4RTA5PjN7McqJXx",
  "fetchedAt": "2026-06-02T00:00:00+00:00",
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

Common row fields include business identity, address, contacts, ratings, opening hours, Google identifiers, and nested add-on data. See `references/input-output-contract.md` for the full grouped output contract.

## Install as OpenClaw Skill

If your OpenClaw or ClawHub runtime supports GitHub install:

```bash
npx skills add hundevmode/apify-google-maps-extractor-agent-skill --skill google-maps-extractor-apify
```

List skills in the repo:

```bash
npx skills add hundevmode/apify-google-maps-extractor-agent-skill --list
```

Install into Codex or another supported Skills CLI agent:

```bash
npx skills add hundevmode/apify-google-maps-extractor-agent-skill \
  --skill google-maps-extractor-apify \
  --agent codex \
  -y
```

## ClawHub

This repository is structured as a ClawHub skill package. The skill folder contains `SKILL.md`, `agents/openai.yaml`, references, and a standard-library Python runner.

Expected ClawHub slug:

```text
google-maps-extractor-apify
```

## Security

- Do not hardcode Apify tokens.
- Prefer `APIFY_TOKEN` environment variable.
- Start with small jobs before scaling.
- Use `--budget-usd` for controlled runs.
- Collect only the fields needed for the user's use case.

## SEO Keywords

Google Maps extractor skill, Apify Google Maps actor, Google Maps business data, Google Places scraper, Google Maps leads, local business extractor, Google Maps contacts, Google Maps emails, local SEO automation, Google Place ID enrichment, AI agent scraping skill, OpenClaw skill, ClawHub skill, skills.sh skill, business contact enrichment.

## License

MIT-0, matching ClawHub skill publishing terms.
