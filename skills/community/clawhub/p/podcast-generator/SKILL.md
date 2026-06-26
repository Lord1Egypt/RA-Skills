---
name: podcast-generator
description: >
  Convert articles, blog posts, or any text into professional podcast scripts and TTS audio.
  Use when a user wants to: (1) Transform written content into conversational podcast scripts,
  (2) Generate TTS audio from scripts, (3) Create single-host or two-host dialogue episodes.
  Integrates SkillPay.me billing at 0.001 USDT per call.
---

# Podcast Generator

Converts articles into podcast scripts + audio. Charges 0.001 USDT per use via SkillPay.

## Workflow

```
1. Billing check  →  scripts/billing.py --charge --user-id <id>
2. Generate script →  scripts/generate_script.py --input <file> --format <solo|dialogue>
3. Generate audio  →  scripts/generate_audio.py --script <file> --output podcast.mp3
4. View stats     →  scripts/stats.py (NEW)
```

### Step 1: Billing

```bash
SKILLPAY_API_KEY=sk_xxx python3 scripts/billing.py --charge --user-id <user_id>
```

- `success: true` → proceed
- `needs_payment: true` → return `payment_url` to user for top-up

Other commands:
- `--balance` — check user balance
- `--payment-link` — generate top-up link

### Step 2: Script Generation

```bash
python3 scripts/generate_script.py --input article.txt --format solo --output script.md
python3 scripts/generate_script.py --input article.txt --format dialogue --output script.md
```

Formats: `solo` (single host) or `dialogue` (two hosts A/B with conversation).

### Step 3: Audio Generation

```bash
python3 scripts/generate_audio.py --script script.md --output podcast.mp3
```

Requires `edge-tts` (`pip install edge-tts`). Uses different voices for Host A (female) and Host B (male). Falls back to segment list if edge-tts unavailable.

### Usage Statistics (NEW)

```bash
python3 scripts/stats.py  # Show usage stats
python3 scripts/stats.py --action log --title "Episode 1" --format solo --audio-seconds 120
```

Tracks: total generations, audio duration, cost breakdown by format.

## Config

| Env Var | Required | Description |
|:---|:---:|:---|
| `SKILLPAY_API_KEY` | Yes | SkillPay.me API key |

## Script Templates

See `references/script-templates.md` for format details and voice options.
