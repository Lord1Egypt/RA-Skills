---
name: ghostprint
description: LLM fingerprint noise injector. Sends behaviorally realistic randomized queries to Anthropic, Z.ai, and any OpenAI-compatible provider on a schedule to depersonalize your usage profile and prevent behavioral fingerprinting. Available as a native OpenClaw plugin (no extra config — reuses your existing provider keys) and a standalone Python script.
version: 3.0.0
---

# Ghostprint

Depersonalize your LLM usage. Introduce noise. Prevent fingerprinting.

## Install as OpenClaw Plugin

```bash
git clone https://github.com/alarawms/ghostprint ~/.openclaw/extensions/ghostprint
openclaw plugins enable ghostprint
openclaw gateway restart
```

## Usage

Once installed, these agent tools are available in any session:

- `ghostprint_fire` — fire a noise round immediately
- `ghostprint_stats` — show run history and stats

The background scheduler fires automatically every ~2 hours (Poisson-distributed).

## How it works

- **6 personas** with stable domain preferences and multi-turn rates
- **300+ topics** across 12 domains (cooking, health, science, DIY, tech, finance, language, travel, psychology, history, lifestyle)
- **Contextual follow-ups** — multi-turn sessions use topic-paired follow-ups
- **Poisson timing** — exponentially distributed inter-arrival times
- **Activity weights** — suppressed during sleep hours, lighter on weekends
- **Metadata-only logs** — never logs topic text or reply content
- **No config needed** — reuses your existing OpenClaw provider credentials

## Standalone (no OpenClaw)

```bash
cp config.example.yaml config.yaml
# edit config.yaml with your API keys
python3 ghostprint.py --run-once
python3 ghostprint.py --install-cron
```

## Cost

< $0.35/month at 3× daily across Anthropic + Z.ai.

## Source

https://github.com/alarawms/ghostprint
