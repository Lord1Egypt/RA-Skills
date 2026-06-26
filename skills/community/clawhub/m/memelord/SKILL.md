---
name: Memelord
summary: Generate memes programmatically using the Memelord API.
description: AI-powered meme generation, meme editing, meme video generation for your projects, powered by memelord.com's trending memetic data
how to get access: get 50 free API credits with a Memelord.com subscription
homepage: https://memelord.com
metadata:
  api:
    key_env: MEMELORD_API_KEY
    url: https://www.memelord.com/docs
  openclaw:
    emoji: "😂"
    requires:
      bins: ["node", "curl", "realpath"]
      env: ["MEMELORD_API_KEY"]
    primaryEnv: MEMELORD_API_KEY
---

# Memelord Skill

Generate image and video memes on demand through the Memelord API with a set of ready-to-run helper scripts.

## Setup

1. **API key** – export it once per shell (or drop it into `.env`).
   ```bash
   export MEMELORD_API_KEY="YOUR_KEY"
   ```
2. **Executable scripts** – the repo ships with `chmod +x` already applied. If you clone from somewhere that strips modes, just run:
   ```bash
   chmod +x scripts/*.sh
   ```
3. (Optional) create an `outputs/` folder to keep downloaded memes tidy:
   ```bash
   mkdir -p /root/.openclaw/workspace/outputs
   ```

## CLI Overview

| Script | Endpoint | Purpose |
| --- | --- | --- |
| `scripts/ai-meme.sh` | `POST /api/v1/ai-meme` | Generate fresh image memes |
| `scripts/ai-meme-edit.sh` | `POST /api/v1/ai-meme/edit` | Edit an existing image meme |
| `scripts/ai-video-meme.sh` | `POST /api/v1/ai-video-meme` | Kick off async video meme renders |
| `scripts/ai-video-meme-edit.sh` | `POST /api/v1/ai-video-meme/edit` | Re-caption an existing video meme |
| `scripts/video-render-remote.sh` | `GET /api/video/render/remote` | Poll render job status / URLs |
| `scripts/verify-webhook.sh` | helper | Validate webhook signatures |

All scripts accept `--out <path>` so you can control where JSON responses land.

### 1. Generate image memes (1 credit)
```bash
./scripts/ai-meme.sh "developer fixing bugs at 3am" --png ./outputs/meme.png
./scripts/ai-meme.sh "when the code works on the first try" --count 3 --png ./outputs/meme_%d.png
```

### 2. Edit an image meme (1 credit)
```bash
./scripts/ai-meme-edit.sh --from ./memelord_ai_meme.json \
  --instruction "make it about javascript instead" --png ./outputs/edited.png

# or supply template metadata manually
./scripts/ai-meme-edit.sh --template-id abc-123 --template-data-file ./template_data.json \
  --instruction "change the top text" --out ./outputs/edit.json
```

### 3. Generate video memes (5 credits, async)
```bash
./scripts/ai-video-meme.sh "when the code works on the first try" --count 2 --out ./outputs/jobs.json

# with webhook callbacks
./scripts/ai-video-meme.sh "ship it" \
  --webhook-url https://example.com/webhook \
  --webhook-secret supersecret
```

### 4. Edit a video meme caption (5 credits, async)
```bash
./scripts/ai-video-meme-edit.sh --template-id abc-123 \
  --caption "When the code works on the first try" \
  --instruction "make it about not knowing why it works" \
  --out ./outputs/video_edit_job.json
```

### 5. Poll video render status
```bash
./scripts/video-render-remote.sh --job-id render-1740524400000-abc12 --out ./outputs/status.json
```

### 6. Verify webhook signatures
```bash
./scripts/verify-webhook.sh --secret "$WEBHOOK_SECRET" --body-file ./payload.json --signature "<hex>"
```

## Sharing memes in chat surfaces (no links, just media)
When you want Telegram/Signal/WhatsApp/etc. to show **only** the meme (no caption/link blob), follow this pattern:

1. **Generate or edit** the meme as usual (`ai-video-meme.sh`, `ai-meme.sh`, etc.).
2. **Poll the job** if it’s a video (`video-render-remote.sh`) until you see `mp4Url` (or `url` for images) in the JSON.
3. **Download the asset** into your workspace. Example for a video:
   ```bash
   curl -sSL "<mp4Url-from-status>" -o ./outputs/hiring_engineers.mp4
   ```
   For images, the `--png` flag already writes the file; otherwise `curl` the `url` the same way.
4. **Send the file itself** back to the chat using the OpenClaw media syntax so only the video/image appears:
   ```
   MEDIA:./outputs/hiring_engineers.mp4
   ```
   *(Swap the extension for `.png`/`.webp` for still memes.)*

Because the attachment is the only thing in the reply, Telegram renders it inline without any auto-generated “description + link” chatter.

---
**Credits:** Memelord gives you 50 video/image credits per month on the base subscription. Top up or read more at https://www.memelord.com/docs.
