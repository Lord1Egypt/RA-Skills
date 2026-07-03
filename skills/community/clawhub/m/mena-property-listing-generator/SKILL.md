---
name: mena-property-listing-generator
version: 1.0.1
author: "NASSER AL-SOLAITTI"
description: "AI-powered bilingual property listing generator for MENA real estate agents. Input: basic property specs. Output: SEO-optimized Arabic + English listing text, Instagram caption, TikTok script, Facebook post, and WhatsApp follow-up scripts. Use when user says 'create property listing', 'real estate listing', 'listing in Arabic', 'PropertyFinder listing', or wants to reduce manual copywriting time.
permissions:
  - network: send listing text and agent details to minimax LLM API (api.minimax.chat) only
  - filesystem-write: write generated listings to ~/.openclaw/mena-property-listing-generator/
  - env: read MINIMAX_API_KEY from environment
privacy: |
  Data sent to LLM: property specs (location, type, price, area, bedrooms, bathrooms, features),
  agent name and phone — NO photos are transmitted. Photos remain on-disk only.
  Local storage: listing JSON files, agent profiles, and monthly counters are stored at
  ~/.openclaw/mena-property-listing-generator/. No data is sent to third parties other than
  the minimax LLM API endpoint.
---

# MENA Property Listing Generator

## When to use this skill

Activate when the user wants to:
- Create a bilingual (Arabic + English) property listing
- Generate social media posts for a new property
- Write WhatsApp follow-up scripts for leads
- Reduce manual copywriting time per listing

## Prerequisites

- Basic specs: bedrooms, bathrooms, sqm, location, price, key features
- MINIMAX_API_KEY set in the environment
- OpenClaw gateway

## Workflow

### 1. Add your agent profile (one-time)

```bash
clawhub run mena-property-listing-generator agents \
  --add \
  --name "Nasser Al-Solaitti" \
  --phone "+974-XXXX-XXXX" \
  --agency "Skyline Real Estate"
```

### 2. Run the listing generator

```bash
clawhub run mena-property-listing-generator new \
  --location "Lusail" \
  --type "2BR Apartment" \
  --price 3100000 \
  --area 250 \
  --bedrooms 2 \
  --bathrooms 2 \
  --features "sea view, fully furnished, 2 parking" \
  --agent "Nasser Al-Solaitti" \
  --phone "+974-XXXX-XXXX"
```

### 4. Review the output

The skill produces in `./listing-001/`:

- `listing-ar.md` — Arabic SEO-optimized listing (for PropertyFinder, Bayut, Dubizzle)
- `listing-en.md` — English SEO-optimized listing
- `instagram-caption.txt` — caption + hashtags
- `tiktok-script.md` — 60-second walkthrough script
- `facebook-post.txt` — Facebook-optimized post
- `whatsapp-scripts.md` — 5 follow-up scripts (cold, warm, hot leads)

> **Coming in v1.1:** Instagram carousel slide images and PDF brochure generation.

### 5. Bulk mode (multiple properties)

```bash
# Folder structure:
# ./specs.csv
# property-001,3BR, 250sqm, Lusail Marina, QAR 3,100,000, ...
# property-002,2BR, 180sqm, West Bay, QAR 2,400,000, ...
# property-003,4BR, 320sqm, Pearl, QAR 4,800,000, ...

clawhub run mena-property-listing-generator bulk \
  --csv ./specs.csv \
  --output ./listings/
```

### 6. Customization per listing

For one-off edits:

```bash
# Reformat a saved listing in WhatsApp, Instagram, or PDF
clawhub run mena-property-listing-generator format \
  --input LST-0001 \
  --format whatsapp

# Or show all formats at once
clawhub run mena-property-listing-generator format \
  --input LST-0001 \
  --format all

# Bulk-generate new listings from a CSV
clawhub run mena-property-listing-generator bulk \
  --csv ./properties.csv
```

## Outputs

For each listing, you get:
- **Bilingual listings** (Arabic + English) — SEO-optimized for the platform
- **Instagram**: caption + hashtags
- **TikTok**: 60-second walkthrough script
- **Facebook**: post + link card
- **WhatsApp scripts**: 5 variants for different lead temperatures

## Time saved

- Manual: 2-4 hours per listing
- With this skill: 5 minutes (review + minor edits)
- At 8 listings/month: 16-32 hours/month saved

## Why MENA-specific

- **Native Arabic copywriting** (not translated — proper dialect + cultural context)
- **RTL-aware** formatting for Arabic output
- **Platform preferences** differ by market (Instagram + WhatsApp dominant in UAE/Qatar)
- **Currency formatting** (QAR, AED, SAR, EGP)
- **Cultural context**: commute times, school districts, family amenities
- **Major platforms** recognized: PropertyFinder, Bayut, Dubizzle

## Common customizations

**For Lusail / Qatar agents:**
- Highlight: Lusail Marina, FIFA Stadium access, Pearl proximity
- Currency: QAR
- Platforms: PropertyFinder Qatar + Instagram
- Tone: family-friendly or luxury

**For Dubai Marina / UAE agents:**
- Highlight: marina views, metro access, beach proximity
- Currency: AED
- Platforms: Bayut + PropertyFinder + Dubizzle
- Tone: luxury or investor-focused

**For Saudi agents (Riyadh/Jeddah):**
- Highlight: district, school zones, compound amenities
- Currency: SAR
- Platforms: Aqar + Bayut Saudi
- Tone: family-friendly

## Cost expectations

- LLM generation: ~$0.05-0.10 per listing (via MINIMAX_API_KEY)
- OpenClaw: free, self-hosted

**Typical usage** (8 listings/month): <$1/month total.

## Troubleshooting

**Listing quality not what you expected?**
- Try adding more specific features to --features ("sea view", "corner unit", "new building")
- Adjust --price and --area for more targeted output

**Need a different format?**
- Use `--format whatsapp`, `--format instagram`, or `--format pdf`

**Bulk generation slow?**
- LLM calls are sequential; expect ~5-10 seconds per listing

## See also

- `references/arabic-copywriting.md` — Arabic tone and dialect guide
- `references/platform-formats.md` — PropertyFinder, Bayut, Dubizzle specs
- `references/whatsapp-scripts.md` — lead qualification flow templates
- `references/brochure-templates.md` — design templates
