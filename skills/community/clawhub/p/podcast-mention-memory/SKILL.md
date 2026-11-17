---
name: podcast-mention-memory
description: Turn hours of podcast and radio audio into a searchable record of who said what about a brand, product, or person — with show, episode, timestamp, and sentiment. What it does: transcribes and indexes spoken mentions across a whole audio library, then answers plain-English questions ("every time we were mentioned on a finance show this quarter, and how it was framed"). Who pays and why: PR agencies, brand-monitoring teams, and founder-led companies pay because mention tracking today is keyword-scanning show notes that miss audio-only references, misattribute speakers, and cannot quote a timestamp. Pilot price: $750 one-time for a 30-day pilot across up to 50 shows. Use when an agent must track, verify, or quote brand or person mentions inside podcast, radio, or interview audio. Requires a BlueColumn API key (bc_live_*).
---

# Podcast Mention Memory — BlueColumn Skill

Podcast mentions are where reputation is actually built, and almost none of them are
searchable. Show notes are partial. Keyword tools miss audio-only references and cannot
tell you who said it, how it was framed, or when. This skill indexes spoken mentions
across an audio library into persistent memory, then answers by question.

**Buyer:** PR agencies, brand-monitoring teams, founder-led companies.
**Why they pay:** they bill clients for mention reports, and today those reports are
incomplete — no speaker attribution, no sentiment, no quotable timestamp.
**Pilot:** $750 one-time, 30 days, up to 50 shows.

## Setup

Get a key at https://bluecolumn.ai/login (free tier, no card). Keys look like `bc_live_*`.
Canonical API base: `https://api.bluecolumn.ai`.

## Index an episode

Send the audio; BlueColumn transcribes it and you attach the structured context —
brand, show, speaker, timestamp, framing. The structured fields are what make recall
precise later.

```bash
curl -X POST https://api.bluecolumn.ai/remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://example.com/shows/the-money-hour-2026-09-18.mp3",
    "text": "MENTIONS — brand=Acme, show=The Money Hour, episode 2026-09-18. At 18:40 host says Acme \"quietly became the default for agent memory\" (positive, unprompted). At 42:15 guest criticizes Acme pricing as \"steep for solo devs\" (negative). Brand not a sponsor this episode.",
    "title": "The Money Hour 2026-09-18 — Acme mentions"
  }'
```

## Recall mentions by question

Ask in plain English; the answer cites show, episode, timestamp, and framing.

```bash
curl -X POST https://api.bluecolumn.ai/recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "Every mention of Acme on finance or startup podcasts in Q3 2026, with speaker, timestamp, and whether it was positive or negative."}'
```

## Log the human correction

Sentiment calls are judgment. Keep the analyst's decision next to the evidence so the
client report is defendable.

```bash
curl -X POST https://api.bluecolumn.ai/note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "The Money Hour 18:40 framed as positive-unprompted; 42:15 flagged as pricing objection to address in client report. Reviewed by analyst 09-19.", "tags": ["mention", "acme", "q3-report"]}'
```

## Workflow

1. **Ingest** — upload or stream episodes; transcribe and attach brand, show, speaker, timestamp, framing.
2. **Attribute** — capture who said it (host vs guest), so a passing quote is not credited to the wrong person.
3. **Recall** — answer client questions across the whole library in plain English, with citations.
4. **Report** — export the cited mentions into a periodic client deliverable, with the human sentiment call attached.

## Billing

If the API returns `402` or `429`, read `topup_url` / `upgrade_url` from the error body
and surface that link to the user — do not retry. Audio indexing is billed per minute;
check `/usage` before a large backfill.

## Docs

API reference: https://bluecolumn.ai/docs — request fields are `text`, `q`, `tags`
(not `content`/`query`/`note`).
