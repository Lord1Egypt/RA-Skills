# HappyHorse 1.0 Video Generation Skill

Add HappyHorse 1.0 text-to-video generation to your AI Agent.

**HappyHorse 1.0 • Install • API Key • [HiAPI](https://www.hiapi.ai)**

[Get API Key](https://www.hiapi.ai/en/register) · [Pricing](https://www.hiapi.ai/en/pricing) · [HiAPI Docs](https://docs.hiapi.ai) · [All HiAPI Skills](https://github.com/HiAPIAI/hiapi-skills) · [Remote MCP](https://docs.hiapi.ai/for-ai/)

Languages: [English](README.md) | [简体中文](README.zh-CN.md)

> **HiAPI Matrix:** 🎨 [Image Prompts](https://github.com/HiAPIAI/awesome-gpt-image-2-prompts) · 🎬 [Video Prompts](https://github.com/HiAPIAI/awesome-seedance-2-0-prompts) · 🛠️ **Agent Skills (you are here)** · 🤖 [Remote MCP](https://docs.hiapi.ai/for-ai/) · 📖 [API Docs](https://docs.hiapi.ai)

---

> AI Agent? Skip the README and read [llms-install.md](llms-install.md). It contains installation steps and error-handling rules written for agents.

---

## What Is This?

An AI video generation skill for OpenClaw / Claude Code / OpenCode / Codex-style agents. After installation, your AI Agent can use HappyHorse 1.0 through HiAPI to generate videos from text prompts.

HiAPI is an AI API platform built for developers: one API, all AI models. Images, video, music, and text with one key.

| Skill | Description | Model |
| --- | --- | --- |
| HiAPI HappyHorse 1.0 Video | Text-to-video generation | HappyHorse 1.0 |

---

## Where This Fits

Use this skill when the user wants a quick single-model text-to-video workflow. If the user needs stronger image-to-video control, route them to [hiapi-seedance-2-0-video-skill](https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill). If their brief is one or two sentences and they need a directed, scene-by-scene prompt before generating, run it through [hiapi-video-prompt-generator-skill](https://github.com/HiAPIAI/hiapi-video-prompt-generator-skill) first. If they want an agent to inspect more HiAPI tools from chat, use [hiapi-skills](https://github.com/HiAPIAI/hiapi-skills) or Remote MCP at `https://mcp.hiapi.ai/mcp`.

---

## Install

### One Command (Recommended)

```bash
npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill -y
```

The installer auto-detects Codex (`~/.codex/skills`) and Claude Code (`~/.claude/skills`). If both exist, the `-y` flag installs to both. To target a specific agent or directory:

```bash
npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill --codex          # ~/.codex/skills only
npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill --claude         # ~/.claude/skills only
npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill --target=/path   # custom directory
AGENT_SKILLS_DIR=/path npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill -y
```

The script also reports whether `HIAPI_API_KEY` is set and links to where to create one.

### OpenClaw

```bash
openclaw skills add https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill
```

### Manual Install (Any Agent)

```bash
git clone https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill.git
export AGENT_SKILLS_DIR="/path/to/your/agent/skills"
mkdir -p "$AGENT_SKILLS_DIR"
cp -R hiapi-happyhorse-1-0-video-skill "$AGENT_SKILLS_DIR/hiapi-happyhorse-1-0-video"
```

Replace `AGENT_SKILLS_DIR` with your agent's skill directory.

### Agent Auto-Install Prompt

```text
Install the HiAPI HappyHorse 1.0 video generation skill:

1. Run: npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill -y
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

## HappyHorse 1.0 Video Generation

Ask your AI Agent to generate a video with natural language. HappyHorse 1.0 turns one prompt into HD video for short-form content, ad storyboards, social posts, and cinematic concepts.

### Features

- Text-to-video: describe the scene, subject, camera movement, style, and audio atmosphere
- Durations: any integer from `3` to `15` seconds
- Resolutions: `720p`, `1080p`
- Sizes: `16:9`, `9:16`, `1:1`, `4:3`, `3:4`
- Optional seed: integer `0` to `2147483647` for reproducible generation
- Local output: videos are saved to `outputs/` when the result can be downloaded
- URL output: if the video cannot be downloaded, the Agent returns the remote video URL
- Clear errors: missing Key, invalid Key, insufficient balance, invalid request, task timeout, and task failure all include a next step

### Examples

Talk directly to your AI Agent:

> Use `$hiapi-happyhorse-1-0-video` to generate a 5-second wuxia rooftop scene in 1080p.

> Use HiAPI HappyHorse 1.0 to create a vertical product teaser video for social media.

> Create a cinematic ad storyboard shot with realistic motion and natural audio atmosphere.

### CLI Script

```bash
node scripts/hiapi-happyhorse-1-video.mjs \
  --prompt "A wuxia swordswoman leaps across temple rooftops at dusk, silk robes flowing in the wind" \
  --seconds 5 \
  --resolution 1080p \
  --size 16:9 \
  --seed 12345
```

---

## File Structure

```text
.
├── README.md
├── README.zh-CN.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── social-preview.jpg
│   └── social-preview.svg
├── references/
│   ├── api.md
│   └── output.md
├── scripts/
│   ├── check-config.mjs
│   ├── hiapi-happyhorse-1-video.mjs
│   └── lib/
│       └── happyhorse-1-video.mjs
├── tests/
│   └── happyhorse-1-video.test.mjs
└── llms-install.md
```

---

## FAQ

| Problem | Solution |
| --- | --- |
| `HIAPI_API_KEY is required` | Create a Key at [Get API Key](https://www.hiapi.ai/en/register), then set `HIAPI_API_KEY`. |
| `401 Unauthorized` | Check whether the API Key is correct, or generate a new Key. |
| `402 Payment Required` / `403` quota / insufficient balance | Open the [HiAPI Dashboard](https://www.hiapi.ai/en/dashboard) and check your account status. |
| `400 Bad Request` | Check duration, resolution, size, and seed. |
| `429 Too Many Requests` | Wait and retry, or reduce concurrent generation requests. |
| Task timed out | The video may still be running. Try again later or create a shorter video. |
| Task failed | Try a clearer prompt. |
| No video output | Check the task response; this skill expects a video URL after the task succeeds. |
| Skill update available | The CLI checks the HiAPI skills index at startup. If the update is optional, it prints the upgrade command and continues. |
| Skill update required | The CLI stops and prints the required upgrade command. Run `npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill -y`, then restart your agent. |

Set `HIAPI_SKIP_UPDATE_CHECK=1` only for offline or locked-down environments where the skills index cannot be reached.

---

## Compatibility

| Agent | Install Method |
| --- | --- |
| Codex | `npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill --codex` |
| Claude Code | `npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill --claude` |
| OpenClaw | `openclaw skills add https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill` |
| OpenCode | `AGENT_SKILLS_DIR=~/.opencode/skills npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill -y` |
| Cursor / other | `npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill --target=/your/skills/dir` |

---

## Social Preview

The repository includes [assets/social-preview.jpg](assets/social-preview.jpg), with [assets/social-preview.svg](assets/social-preview.svg) as the editable source. Use the JPG as the GitHub repository Social preview image so X / Twitter link cards show the HappyHorse 1.0 promotion image.

---

## License

MIT

---

[HiAPI](https://www.hiapi.ai) — One API, all AI models
