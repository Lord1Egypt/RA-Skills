# best-image-generation

> 🎨 High-quality AI image generation & editing for OpenClaw, powered by [WellAPI](https://wellapi.ai) `gpt-image-2`.

A drop-in OpenClaw skill that gives your agent the ability to:

- **Text-to-image** — generate images from a natural-language prompt.
- **Image editing / image-to-image** — modify one or more local images with a prompt (optional mask for inpainting).
- Resolutions from `1024×1024` up to **4K** (`3840×2160` / `2160×3840`).
- Synchronous responses — base64 bytes come back inline, no polling, no URL fetch.
- Auto-attach generated images into your OpenClaw conversation via the `MEDIA:<path>` line protocol.

---

## Quick start

### 1. Install the skill

From an OpenClaw-enabled client (Claude Code / OpenClaw CLI):

```bash
clawhub install best-image-generation
```

Or drop this folder under your OpenClaw skills directory.

### 2. Set your API key

The skill reads its credential from a single environment variable:

```bash
# macOS / Linux
export WELLAPI_API_KEY="sk-..."

# Windows (PowerShell)
$env:WELLAPI_API_KEY = "sk-..."
```

Get a key from <https://wellapi.ai>. If the env var is not set, the skill will prompt for it before running.

### 3. Trigger it

| Intent | Chinese trigger | English trigger |
|---|---|---|
| Text-to-image | `高质量生图：一只在月球上读报的柴犬` | `best image: a shiba inu reading a newspaper on the moon` |
| Image edit | `编辑图片：把背景换成赛博朋克霓虹街道` (+ 附图) | `edit image: replace background with cyberpunk neon street` (+ attach files) |

Text after the colon becomes the `prompt`. Defaults: `size=auto`, `quality=auto`, `format=png`, `n=1`.

---

## What's in the box

```
image-generation-gpt/
├── SKILL.md              # Skill definition + frontmatter (ClawHub manifest)
├── README.md             # You are here
├── CHANGELOG.md          # Version history
├── _meta.json            # ClawHub publish metadata
├── examples/
│   ├── basic.md          # Simple text-to-image walkthrough
│   └── advanced.md       # Multi-image edit + mask + 4K
└── references/
    ├── python.md         # Python 3 reference implementation (zero deps)
    ├── powershell.md     # PowerShell 5.1+ reference (Windows)
    └── curl_heredoc.md   # curl + bash reference (Unix/macOS)
```

The agent picks the reference implementation that matches the host platform.

---

## API surface (summary)

Full details live in [SKILL.md](./SKILL.md). Cheat sheet:

| Endpoint | Method | Content-Type | Purpose |
|---|---|---|---|
| `https://wellapi.ai/v1/images/generations` | POST | `application/json` | Text-to-image |
| `https://wellapi.ai/v1/images/edits` | POST | `multipart/form-data` | Image edit / img2img |

Common knobs:

- `model` — defaults to `gpt-image-2`. Edit endpoint also accepts `gpt-image-1`, `flux-kontext-pro`, `flux-kontext-max`, etc.
- `n` — 1–10 images per call.
- `size` — `1024x1024` / `1536x1024` / `1024x1536` / `2048x2048` / `2048x1152` / `3840x2160` / `2160x3840` / `auto`.
- `quality` — `low` / `medium` / `high` / `auto`.
- `format` — `png` / `jpeg` / `webp`.

Custom sizes must obey: longest side ≤ 3840px, both dims multiple of 16, aspect ratio ≤ 3:1, total pixels in `[655 360, 8 294 400]`.

---

## Output protocol

Every generated image is:

1. Base64-decoded from `response.data[i].b64_json`.
2. Written to `wellapi-<TIMESTAMP>.<ext>` (suffixed `-1`, `-2`, … when `n > 1`).
3. Announced on stdout as `MEDIA:<absolute_path>` — OpenClaw auto-attaches it to the chat.

Filenames are sanitized (`tr -cd 'A-Za-z0-9._-'`) before any shell interpolation. Extension is validated against `.png / .jpg / .jpeg / .webp`.

---

## Requirements

- An OpenClaw-compatible host (Claude Code / OpenClaw CLI / clawd).
- `WELLAPI_API_KEY` environment variable.
- One of: Python 3.6+ **or** PowerShell 5.1+ **or** `curl` — the skill picks whichever is available.

No SDK install required. The reference implementations rely only on the language's standard library.

---

## Limits & cost notes

- **Prompt** ≤ 1000 characters.
- **Edit input**: up to **16** reference images per request, total ≤ **50 MB**.
- **Mask**: PNG only, < 4 MB, same dimensions as the image it applies to.
- `quality: high` and large `size` values incur higher per-image cost — see <https://wellapi.ai> pricing.

---

## Links

- Skill manifest: [SKILL.md](./SKILL.md)
- Changelog: [CHANGELOG.md](./CHANGELOG.md)
- Examples: [examples/basic.md](./examples/basic.md), [examples/advanced.md](./examples/advanced.md)
- Provider: <https://wellapi.ai>
- Issues / feedback: file via the ClawHub skill page.

---

## License

Published on ClawHub under **MIT-0**. You may use, modify, and redistribute this skill freely, including commercially. Attribution not required.
