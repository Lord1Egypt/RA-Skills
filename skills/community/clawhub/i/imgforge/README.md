# zimage — Free AI Image Generation Skill

<p align="center">
  <img src="./icon.png" alt="Z-Image Skill" width="128" height="128">
</p>

<p align="center">
  <strong>Turn text into images for free, right from your AI coding assistant.</strong><br>
  Works with Claude Code · OpenClaw · Codex · Antigravity · Paperclip
</p>

<p align="center">
  <a href="./README.md">English</a> ·
  <a href="./docs/README_TW.md">繁體中文</a> ·
  <a href="./docs/README_JA.md">日本語</a> ·
  <a href="./docs/README_KO.md">한국어</a> ·
  <a href="./docs/README_ES.md">Español</a> ·
  <a href="./docs/README_DE.md">Deutsch</a> ·
  <a href="./docs/README_FR.md">Français</a> ·
  <a href="./docs/README_IT.md">Italiano</a>
</p>

---

## Overview

**zimage** gives your AI assistant the ability to generate images from natural language. It calls [Z-Image-Turbo](https://github.com/Tongyi-MAI/Z-Image) — an open-source 6B-parameter model by Alibaba's Tongyi-MAI team — through ModelScope's free API.

```
You:  Create an image of a fox reading a book in a library
AI:   Submitting: a fox reading a book in a library
      Task 91204 — waiting for result…
      Saved → fox_library.jpg
```

### How it compares

|  | zimage | DALL-E 3 | Midjourney |
|--|--------|----------|------------|
| Price | **Free** | $0.04–0.08 / image | From $10/mo |
| Open source | Apache 2.0 | No | No |
| Setup time | ~5 min | Billing required | Discord required |

> **Free tier:** 2,000 API calls/day total, 500/day per model. Limits may be dynamically adjusted. ([official limits](https://modelscope.ai/docs/model-service/API-Inference/limits))

---

## Setup

### 1 — Alibaba Cloud account (free)

Register at **https://www.alibabacloud.com/campaign/benefits?referral_code=A9242N**

You'll need to verify your phone number and add a payment method during registration. **Z-Image itself is free and will not charge you**, but Alibaba Cloud requires payment info on file for all accounts.

### 2 — ModelScope account + binding

1. Go to **https://modelscope.ai/register?inviteCode=futurizerush&invitorName=futurizerush&login=true&logintype=register** → sign up (GitHub login works)
2. Open **Settings → Bind Alibaba Cloud Account** and link the account from step 1

### 3 — API token

1. Visit **https://modelscope.ai/my/access/token**
2. Click **Create Your Token**
3. Copy it — looks like `ms-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

---

## Install

<details>
<summary><b>Claude Code</b></summary>

Say this in Claude Code:

```
Install the zimage skill from https://github.com/FuturizeRush/zimage-skill
```

Then:

```
Set my MODELSCOPE_API_KEY environment variable to ms-your-token
```

Restart Claude Code.
</details>

<details>
<summary><b>OpenClaw / ClawHub</b></summary>

```bash
openclaw skills install zimage
# or
npx clawhub@latest install zimage
```

```bash
export MODELSCOPE_API_KEY="ms-your-token"
```
</details>

<details>
<summary><b>Codex / Antigravity / Paperclip / Other</b></summary>

```bash
git clone https://github.com/FuturizeRush/zimage-skill.git
cd zimage-skill
pip install Pillow  # optional, for format conversion
export MODELSCOPE_API_KEY="ms-your-token"
```

```bash
python3 imgforge.py "a sunset over the ocean" sunset.jpg
```
</details>

---

## Usage

### Through your AI assistant

Just ask naturally:

```
Generate an image of a cozy coffee shop, warm lighting, cinematic
Draw a pixel-art dragon breathing fire
Create a minimalist logo, blue gradients, clean vector style
```

### Direct CLI

```bash
# Basic
python3 imgforge.py "a cat astronaut on Mars"

# Custom size (landscape)
python3 imgforge.py "mountain panorama at golden hour" -o panorama.jpg -W 2048 -H 1024

# Machine-readable output
python3 imgforge.py "abstract art" --json
# → {"ok": true, "path": "output.jpg", "task": "91204"}
```

### CLI flags

| Flag | Default | Description |
|------|---------|-------------|
| `prompt` | *(required)* | What to generate |
| `-o` / `--out` | `output.jpg` | Output path (.jpg, .png, .webp) |
| `-W` / `--width` | `1024` | Width, 512–2048 px |
| `-H` / `--height` | `1024` | Height, 512–2048 px |
| `--json` | off | JSON output for scripting |

### Prompt tips

**Quality boosters:** `4K`, `cinematic`, `professional photography`, `dramatic lighting`, `shallow depth of field`

**Style keywords:** `oil painting`, `watercolor`, `anime`, `pixel art`, `ink wash`, `blueprint`, `isometric`

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `MODELSCOPE_API_KEY is not set` | See [Setup](#setup) above |
| `401 Unauthorized` | Use **modelscope.ai** (not .cn). Bind Alibaba Cloud in settings. Regenerate token. |
| Timeout | API under load — retry in a minute |
| Content moderation | Rephrase your prompt |

---

## Technical notes

- **Zero required dependencies** — uses Python's `urllib.request`. Pillow is optional (auto-detected for format conversion).
- Supports custom image dimensions from 512×512 to 2048×2048.
- `--json` flag enables integration with other tools and scripts.
- Image URLs from the API expire in 24h — the script downloads immediately.
- Model: [Tongyi-MAI/Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) (Apache 2.0)
- API: ModelScope International (`api-inference.modelscope.ai`)

---

## License

MIT-0 — do whatever you want with it.
