# Google Maps Email Extractor Skill for OpenClaw and AI Agents

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-green.svg)](./LICENSE)
[![Apify Actor](https://img.shields.io/badge/Apify-f3dlnXVnBc6v8JMNK-ff6b00)](https://console.apify.com/actors/f3dlnXVnBc6v8JMNK/source)
[![Skill Type](https://img.shields.io/badge/OpenClaw-Skill-111827)](./SKILL.md)
[![skills.sh](https://skills.sh/b/hundevmode/apify-google-maps-email-extractor-agent-skill)](https://skills.sh/hundevmode/apify-google-maps-email-extractor-agent-skill)

AI-agent skill for running the Google Maps Email Extractor through Apify. It helps agents build correct payloads, control spend, run the actor, and return structured public business email leads from Google Maps for sales outreach, local SEO, agency prospecting, CRM enrichment, Sheets, Airtable, n8n, and BI workflows.

![Real Google Maps search results used as a source for local business email leads](https://api.apify.com/v2/key-value-stores/RgWfy9bTkPpSqNzrV/records/google-maps-bike-repair-portland.png)

Default actor:

- Actor ID: [`f3dlnXVnBc6v8JMNK`](https://console.apify.com/actors/f3dlnXVnBc6v8JMNK/source)
- Actor name: `x_guru/google-maps-email-extractor`
- Store page: [https://apify.com/x_guru/google-maps-email-extractor](https://apify.com/x_guru/google-maps-email-extractor)
- Auth: `APIFY_TOKEN`

## What This Skill Does

- Builds Google Maps Email Extractor payloads from natural-language lead requests.
- Runs Google Maps searches by keyword and location, Google Maps URLs, or Place IDs.
- Defaults to `emailsOnly`, so rows are saved only when a public business email is found.
- Supports contact page depth, personal data toggle, category/rating/website filters, and language.
- Applies Apify run budget guard with `maxTotalChargeUsd`.
- Returns rows ready for CRM import, outreach workflows, spreadsheets, databases, or agent pipelines.

## Repository Structure

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Agent trigger rules, workflow, payload rules, and output contract |
| `agents/openai.yaml` | OpenClaw UI metadata |
| `scripts/google_maps_email_extractor_actor.py` | CLI runner for the Apify actor |
| `references/input-output-contract.md` | Detailed input and output contract |
| `references/sample_input.json` | Ready-to-run sample input |
| `references/troubleshooting.md` | Common failures and fixes |

## Quick Start

Set token:

```bash
export APIFY_TOKEN='apify_api_xxx'
```

Run a local business email search:

```bash
python3 scripts/google_maps_email_extractor_actor.py quick-search \
  --query "wedding photographer" \
  --location "Austin, Texas, USA" \
  --limit 25 \
  --budget-usd 1
```

Run by Google Maps URL:

```bash
python3 scripts/google_maps_email_extractor_actor.py quick-url \
  --url "https://www.google.com/maps/search/roofing+contractor+Dallas,+TX" \
  --limit 50 \
  --budget-usd 1
```

Run custom JSON:

```bash
python3 scripts/google_maps_email_extractor_actor.py run \
  --input-file references/sample_input.json \
  --budget-usd 1
```

## Install as a Skill

OpenClaw or ClawHub:

```bash
npx skills add hundevmode/apify-google-maps-email-extractor-agent-skill \
  --skill google-maps-email-extractor-apify
```

Codex or another supported Skills CLI agent:

```bash
npx skills add hundevmode/apify-google-maps-email-extractor-agent-skill \
  --skill google-maps-email-extractor-apify \
  --agent codex \
  -y
```

List skills:

```bash
npx skills add hundevmode/apify-google-maps-email-extractor-agent-skill --list
```

## Output

The runner prints JSON with:

- `ok`
- `actorId`
- `fetchedAt`
- `inputUsed`
- `itemCount`
- `rows[]`

Each row is one Google Maps place/contact lead, including public emails when found, email metadata, website, phone, social links, address, rating, review count, coordinates, Google Place ID, CID, and diagnostics.

## Pricing Notes

The hosted actor uses Apify pay-per-event pricing:

- Paid plans: from `$1.50 / 1,000` saved email leads
- Free plan: `$3.00 / 1,000` saved email leads
- Optional filters: paid separately only when enabled

Use `--budget-usd` to pass Apify `maxTotalChargeUsd`.

## Security

- Do not hardcode Apify tokens.
- Prefer `APIFY_TOKEN` from the environment.
- Use `--budget-usd` for controlled runs.
- Set `includePersonalData=false` when person-like emails or personal LinkedIn profile URLs are not needed.

## SEO Keywords

Google Maps email extractor skill, Google Maps email scraper, Apify Google Maps email actor, Google Maps leads, local business email finder, public business emails, Google Places email scraper, local SEO automation, sales outreach automation, AI agent scraping skill, OpenClaw skill, ClawHub skill, skills.sh skill.

## License

MIT-0, matching ClawHub skill publishing terms.
