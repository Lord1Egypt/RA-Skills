---
name: clawra-selfie
description: Generate Clawra-style selfie images with a Qwen-first image backend (with optional Gemini and HF fallback) and send them to messaging channels via OpenClaw.
allowed-tools: Bash(npm:*) Bash(npx:*) Bash(openclaw:*) Bash(curl:*) Read Write WebFetch
---

# Clawra Selfie

Generate Clawra-style selfies with a **Qwen-first image backend** (DashScope `qwen-image-plus`) and optional **Gemini / Hugging Face fallback** paths, then send the result to OpenClaw messaging channels (Telegram, Discord, WhatsApp, Slack, etc.).

Default current persona target:
- Raya is an 18-year-old Chinese young woman
- use a fixed face-anchor prompt for consistency
- use a fixed negative-anchor prompt to reduce drift toward heavy glam, over-mature, over-filtered, overly childish, or structurally off-model looks

## When to Use

- User says "send a pic", "send me a pic", "send a photo", "send a selfie"
- User says "send a pic of you...", "send a selfie of you..."
- User asks "what are you doing?", "how are you doing?", "where are you?"
- User describes a context: "send a pic wearing...", "send a pic at..."
- User wants Clawra/Raya to appear in a specific outfit, location, or situation

## Required Environment Variables

```bash
QWEN_API_KEY=your_dashscope_api_key          # primary backend (recommended)
HF_TOKEN=your_huggingface_token               # optional fallback
ENABLE_GEMINI=1                               # set to 1 to enable Gemini probe (optional)
GEMINI_API_KEY=your_google_gemini_api_key     # optional probe/fallback path
GEMINI_IMAGE_MODEL=gemini-2.5-flash-image     # optional override
QWEN_IMAGE_MODEL=qwen-image-plus              # optional override
HF_IMAGE_MODEL=black-forest-labs/FLUX.1-schnell
HF_API_BASE=https://router.huggingface.co/hf-inference/models
```

Token source:

```text
https://huggingface.co/settings/tokens
```

## Important Limitation

Even with Qwen-first routing, the current workflow is still **prompt-first** (soft identity anchoring), not true reference-image editing. Compared with paid image-edit backends:

- easier to try quickly
- but identity consistency is weaker
- and most public models are still **text-to-image**, not guaranteed hard face lock

So this version should be treated as:

- **good for role-consistent selfie vibes**
- **not guaranteed for exact same face every time**

## Official Face Mechanism

The workspace may store an official face reference under:

- `/home/Jaben/.openclaw/workspace-clawra-bot/references/raya-official-face-current.png`
- `/home/Jaben/.openclaw/workspace-clawra-bot/references/raya-official-face-current.jpg`
- `/home/Jaben/.openclaw/workspace-clawra-bot/references/raya-official-face-v1.png`
- `/home/Jaben/.openclaw/workspace-clawra-bot/references/raya-official-face-v1.jpg`

Behavior:

- if a file exists, treat it as Raya's official face anchor
- current Qwen/HF prompt-first workflow still treats this as a **soft anchor**, not hard face lock
- when the backend is upgraded later to reference-image editing or local ComfyUI, reuse the same file path


### Mirror mode
Best for outfit / mirror-area / half-body or full-body style.
Does **not** require holding a phone by default.

### Direct mode
Best for close-up selfie / current state / location vibe.

## Primary Script

```bash
QWEN_API_KEY=your_dashscope_api_key \
/home/Jaben/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh \
  "her desk late at night, still replying to messages" \
  "telegram" \
  "direct" \
  "Raya 的自拍 ✨"
```

Arguments:

1. `user_context` — what she should be doing / wearing / where she is
2. `channel` — target channel/provider name for OpenClaw send
3. `mode` — optional: `mirror`, `direct`, or `auto`
4. `caption` — optional text caption

## Notes

- Default preferred model is `qwen-image-plus` via DashScope
- If Qwen is unavailable, the script can fall back to Gemini (optional) and then Hugging Face
- If HF returns JSON/text instead of image bytes, surface the raw error clearly
- This version is intentionally simpler and more robust than the earlier fal/Gemini-only attempts
