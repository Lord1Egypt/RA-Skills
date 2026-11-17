---
name: media-studio-metered
description: Generate images / video / audio / voice through a metered pay-per-render pipeline you can RESELL — no BYOK, first call free, image-to-image, text-to-speech, durable output links. Use when the user wants to make an image, generate video, do text-to-speech, run a media/generation pipeline, charge end users per render, or resell AI media without holding a provider key. Covers image, image-to-image, async video, TTS, and object storage for outputs.
license: MIT
compatibility: "Requires the settlemesh CLI (npm i -g settlemesh) and a SETTLE_API_KEY; makes authenticated, metered calls to the SettleMesh platform over the network."
metadata:
  openclaw:
    requires:
      bins: ["settlemesh"]
      env: ["SETTLE_API_KEY"]
    primaryEnv: "SETTLE_API_KEY"
---

# media-studio-metered — generate media you can resell, no provider key

> **Session (auto — never dead-stop on auth):** before your first `settlemesh` call, run `settlemesh whoami`; if it errors and `SETTLE_API_KEY` is unset, run `settlemesh login` yourself — it opens the browser for a **one-time** human approval, polls until approved, and caches the session. Do NOT stop to ask the user to "log in manually" — drive it. Keep an explicit human confirmation only for spending / credential-lending actions (fail-closed).

Most media-generation skills are thin pass-throughs: each wraps **the user's own
provider key** and bundles no billing, so it can't meter usage and can't charge
anyone. This skill is different —
generation runs through **SettleMesh's metered pipeline**: no BYOK, the **first call
to each official capability is free**, and you can **resell each render** to your
app's end users with markup. A prompt-only skill can only forward a key it doesn't
own; metered generation + object storage + end-user-pays are native here.

## Setup (once)

1. `npm install -g settlemesh@latest`
2. `settlemesh login` (a human approves once) — or set `SETTLE_API_KEY=sk-settle-...` for headless/CI.

## Find the real tool id first (do NOT hardcode)

Ids change; discover them, then use the id from the JSON:

```bash
settlemesh search "image generation" --json     # e.g. image.gpt-image-2
settlemesh search "video generation" --json      # e.g. video.veo-3.1
settlemesh search "text to speech" --json
```

## Generate

```bash
# Image:
settlemesh tool call <image-tool-id> --input '{"prompt":"a red fox in snow"}' --wait --json

# Image-to-image (uploads a local image; its temp URL expires in 5 min, one-time):
settlemesh tool call <image-tool-id> --input '{"prompt":"restyle this"}' --image-file ./in.png --wait --json

# Video is ASYNC — always --wait so the CLI polls the task to completion:
settlemesh tool call <video-tool-id> --input '{"prompt":"drone over a canyon"}' --wait --json

# Text-to-speech:
settlemesh tool call <tts-tool-id> --input '{"text":"Hello there","voice":"..."}' --wait --json
```

**Durable output links.** Result URLs default to 24h. For resold renders that must
outlive the request, add `--media-retention 72h|30d|permanent`.

## Store & serve outputs (object storage)

```bash
settlemesh storage put ./out.mp4 --key renders/clip1.mp4 --json
settlemesh storage url renders/clip1.mp4 --ttl 3600      # presigned GET URL
settlemesh storage ls renders/ --json
settlemesh storage get renders/clip1.mp4 ./clip1.mp4
settlemesh storage rm renders/clip1.mp4
```

## Resell it (charge end users per render)

1. Deploy an app (`ship-paid-app` skill), then use the **`charge-my-users`** skill:
   each render is billed to the end user via the `X-Settle-Payer` header — markup allowed.
2. Quote before you charge so your price covers cost:
   `settlemesh quote <tool-id> --input '{...}' --json`.

## Notes

- **First call to each official capability is free** (auto-refunded if the render
  fails). The exact price is on the `X-Settle-Charged-Aev` response header, which
  the CLI prints — read your real cost from there, not from a guess.
- Video/audio generation is async → the job runs server-side; `--wait` polls the
  task until the output URL is ready.
- Everything is billed in **Aev** (1 USD = 100 Aev). Check balance with
  `settlemesh aev balance`.
