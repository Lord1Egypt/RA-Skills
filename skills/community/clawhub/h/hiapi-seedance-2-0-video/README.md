# Seedance 2.0 Video Generation Skill

Add Seedance 2.0 video generation to your AI Agent.

**Seedance 2.0 • Install • API Key • [HiAPI](https://www.hiapi.ai)**

[Get API Key](https://www.hiapi.ai/en/register) · [Pricing](https://www.hiapi.ai/en/pricing) · [HiAPI Docs](https://docs.hiapi.ai) · [All HiAPI Skills](https://github.com/HiAPIAI/hiapi-skills) · [Remote MCP](https://docs.hiapi.ai/for-ai/)

Languages: [English](README.md) | [简体中文](README.zh-CN.md)

> **HiAPI Matrix:** 🎨 [Image Prompts](https://github.com/HiAPIAI/awesome-gpt-image-2-prompts) · 🎬 [Video Prompts](https://github.com/HiAPIAI/awesome-seedance-2-0-prompts) · 🛠️ **Agent Skills (you are here)** · 🤖 [Remote MCP](https://docs.hiapi.ai/for-ai/) · 📖 [API Docs](https://docs.hiapi.ai)

---

> AI Agent? Skip the README and read [llms-install.md](llms-install.md). It contains installation steps and error-handling rules written for agents.

---

## What Is This?

An AI video generation skill for OpenClaw / Claude Code / OpenCode / Codex-style agents. After installation, your AI Agent can use Seedance 2.0 through HiAPI to generate videos from text or animate an image.

HiAPI is an AI API platform built for developers: one API, all AI models. Images, video, music, and text with one key.

| Skill | Description | Model |
| --- | --- | --- |
| HiAPI Seedance 2.0 Video | Text-to-video and image-to-video | Seedance 2.0 |

---

## Where This Fits

Use this skill when the user needs a stronger video workflow, especially text-to-video plus image-to-video. If the user needs a fast lightweight text-to-video draft, route them to [hiapi-happyhorse-1-0-video-skill](https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill). If their brief is one or two sentences and they need a directed, scene-by-scene prompt before generating, run it through [hiapi-video-prompt-generator-skill](https://github.com/HiAPIAI/hiapi-video-prompt-generator-skill) first. If they need a still-image starting point before animation, use [awesome-gpt-image-2-prompts](https://github.com/HiAPIAI/awesome-gpt-image-2-prompts). For broader agent discovery, use [hiapi-skills](https://github.com/HiAPIAI/hiapi-skills) or Remote MCP at `https://mcp.hiapi.ai/mcp`.

---

## Install

### One Command (Recommended)

```bash
npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill -y
```

The installer auto-detects Codex (`~/.codex/skills`) and Claude Code (`~/.claude/skills`). If both exist, the `-y` flag installs to both. To target a specific agent or directory:

```bash
npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill --codex          # ~/.codex/skills only
npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill --claude         # ~/.claude/skills only
npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill --target=/path   # custom directory
AGENT_SKILLS_DIR=/path npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill -y
```

The script also reports whether `HIAPI_API_KEY` is set and links to where to create one.

### OpenClaw

```bash
openclaw skills add https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill
```

### Manual Install (Any Agent)

```bash
git clone https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill.git
export AGENT_SKILLS_DIR="/path/to/your/agent/skills"
mkdir -p "$AGENT_SKILLS_DIR"
cp -R hiapi-seedance-2-0-video-skill "$AGENT_SKILLS_DIR/hiapi-seedance-2-0-video"
```

Replace `AGENT_SKILLS_DIR` with your agent's skill directory.

### Agent Auto-Install Prompt

```text
Install the HiAPI Seedance 2.0 video generation skill:

1. Run: npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill -y
   (auto-detects Codex / Claude Code skill directories)
2. Set the HIAPI_API_KEY environment variable from https://www.hiapi.ai/en/dashboard/api-keys
3. Read SKILL.md for usage
```

---

## Get API Key

1. Open [Get API Key](https://www.hiapi.ai/en/register)
2. Sign in or create a HiAPI account
3. Create a new API Key
4. Set the environment variable in the terminal that runs your agent:

```bash
export HIAPI_API_KEY="your_hiapi_api_key_here"
export HIAPI_BASE_URL="https://api.hiapi.ai"
```

Check configuration:

```bash
node scripts/check-config.mjs
```

Live check:

```bash
node scripts/check-config.mjs --live
```

---

## Seedance 2.0 Video Generation

Ask your AI Agent to generate a video with natural language. If you provide an image, Seedance 2.0 can use it as the starting frame and turn it into motion.

### Features

- Text-to-video: describe a scene, camera movement, mood, and sound atmosphere
- Image-to-video: provide a public image URL or data URI and describe how it should move
- Durations: any integer from `4` to `15` seconds
- Resolutions: `480p`, `720p`, `1080p`
- Ratios: `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9`, `adaptive`
- Media modes: text-to-video, first-frame image-to-video, first+last-frame image-to-video, or multimodal references
- Generated audio is on by default (API default); pass `--no-audio` to disable, `--generate-audio` to force on
- Reproducible output: pass `--seed <0-2147483647>`
- Local output: videos are saved to `outputs/` when the result can be downloaded
- URL output: if the video cannot be downloaded, the Agent returns the remote video URL
- Clear errors: missing Key, invalid Key, insufficient balance, invalid image URL, task timeout, and task failure all include a next step

### Examples

Talk directly to your AI Agent:

> Use `$hiapi-seedance-2-0-video` to generate a 5-second cinematic ocean cliff video.

> Use HiAPI Seedance 2.0 to create a vertical product teaser video, 9:16 style.

> Animate this product photo with soft camera movement and studio lighting.

### CLI Script

Text-to-video:

```bash
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "A cinematic shot of ocean waves crashing against cliffs at golden hour" \
  --seconds 5 \
  --resolution 720p \
  --ratio 16:9
```

Image-to-video:

```bash
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "The product photo comes alive with soft camera movement and studio lighting" \
  --first-frame-url "https://example.com/product.jpg" \
  --seconds 5
```

First+last-frame image-to-video:

```bash
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "Animate from the first frame to the final hero frame" \
  --first-frame-url "asset://first-frame" \
  --last-frame-url "asset://last-frame" \
  --seconds 5
```

With generated audio:

```bash
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "A coffee shop scene with natural background ambience" \
  --seconds 5 \
  --generate-audio
```

Multimodal reference mode:

```bash
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "Use the reference images, video motion, and audio mood to create a product spot" \
  --reference-image-url "asset://image-1" \
  --reference-video-url "asset://video-1" \
  --reference-video-duration 6 \
  --reference-audio-url "asset://audio-1" \
  --reference-audio-duration 5 \
  --seconds 5
```

Media modes are mutually exclusive: first-frame image-to-video, first+last-frame image-to-video, and multimodal reference mode cannot be mixed in one request. If you need strict first and last frames, use first+last-frame mode. If you need references plus a start/end idea, describe which reference should act as the first or last frame in the prompt.

Reference material limits:

- `reference_image_urls` plus first/last-frame images: at most 9 images total.
- `reference_video_urls`: at most 3 videos; each 2-15 seconds; total duration at most 15 seconds.
- `reference_audio_urls`: at most 3 audio clips; each 2-15 seconds; total duration at most 15 seconds.

---

## File Structure

```text
.
├── README.md
├── README.zh-CN.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── api.md
│   └── output.md
├── scripts/
│   ├── check-config.mjs
│   ├── hiapi-seedance-2-video.mjs
│   └── lib/
│       └── seedance-2-video.mjs
├── tests/
│   └── seedance-2-video.test.mjs
└── llms-install.md
```

---

## FAQ

| Problem | Solution |
| --- | --- |
| `HIAPI_API_KEY is required` | Create a Key at [Get API Key](https://www.hiapi.ai/en/register), then set `HIAPI_API_KEY`. |
| `401 Unauthorized` | Check whether the API Key is correct, or generate a new Key. |
| `402 Payment Required` / `403` quota / insufficient balance | Open the [HiAPI Dashboard](https://www.hiapi.ai/en/dashboard) and check your account status. |
| `400 Bad Request` | Check duration, resolution, ratio, media mode, reference counts, and reference audio/video durations. |
| `429 Too Many Requests` | Wait and retry, or reduce concurrent generation requests. |
| Task timed out | The video may still be running. Try again later or create a shorter video. |
| Task failed | Try a clearer prompt or a different image. |
| No video output | Check the task response; this skill expects a video URL after the task succeeds. |
| Skill update available | The CLI checks the HiAPI skills index at startup. If the update is optional, it prints the upgrade command and continues. |
| Skill update required | The CLI stops and prints the required upgrade command. Run `npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill -y`, then restart your agent. |

Set `HIAPI_SKIP_UPDATE_CHECK=1` only for offline or locked-down environments where the skills index cannot be reached.

---

## Compatibility

| Agent | Install Method |
| --- | --- |
| Codex | `npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill --codex` |
| Claude Code | `npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill --claude` |
| OpenClaw | `openclaw skills add https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill` |
| OpenCode | `AGENT_SKILLS_DIR=~/.opencode/skills npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill -y` |
| Cursor / other | `npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill --target=/your/skills/dir` |

---

## License

MIT

---

[HiAPI](https://www.hiapi.ai) — One API, all AI models
