# GPT Image 2 Image Generation Skill

Add GPT Image 2 image generation to your AI Agent.

**GPT Image 2 • Install • API Key • [HiAPI](https://www.hiapi.ai)**

[Get API Key](https://www.hiapi.ai/en/register) · [Pricing](https://www.hiapi.ai/en/pricing) · [HiAPI Docs](https://docs.hiapi.ai) · [Prompt Gallery](https://github.com/HiAPIAI/awesome-gpt-image-2-prompts) · [All HiAPI Skills](https://github.com/HiAPIAI/hiapi-skills)

Languages: [English](README.md) | [简体中文](README.zh-CN.md)

> **HiAPI Matrix:** 🎨 [Image Prompts](https://github.com/HiAPIAI/awesome-gpt-image-2-prompts) · 🎬 [Video Prompts](https://github.com/HiAPIAI/awesome-seedance-2-0-prompts) · 🛠️ **Agent Skills (you are here)** · 🤖 [Remote MCP](https://docs.hiapi.ai/for-ai/) · 📖 [API Docs](https://docs.hiapi.ai)

---

> AI Agent? Skip the README and read [llms-install.md](llms-install.md). It contains installation steps and error-handling rules written for agents.

---

## What Is This?

An AI skill for OpenClaw / Claude Code / OpenCode / Codex-style agents. After installation, your AI Agent can use GPT Image 2 for image generation through HiAPI.

HiAPI is an AI API platform built for developers: one API for all AI models. Images, video, music, and text with one key.

| Skill | Description | Model |
| --- | --- | --- |
| HiAPI GPT Image 2 | Text-to-image and image-to-image generation | GPT Image 2 family |

---

## Before You Generate

Need a tested starting point? Browse [Awesome GPT Image 2 Prompts](https://github.com/HiAPIAI/awesome-gpt-image-2-prompts) first. It contains output-backed visual recipes with full prompts, aspect ratios, HiAPI Draw links, and source attribution. Pick a recipe, replace the subject, product, city, brand, or copy, then use this skill to generate the adapted result.

If the generated image is meant as the starting frame of a video, plan the motion afterward with [hiapi-video-prompt-generator-skill](https://github.com/HiAPIAI/hiapi-video-prompt-generator-skill), then render with [hiapi-seedance-2-0-video-skill](https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill) (image-to-video).

For broader agent integration, use [hiapi-skills](https://github.com/HiAPIAI/hiapi-skills) as the directory or connect Remote MCP at `https://mcp.hiapi.ai/mcp`.

---

## Install

### One Command (Recommended)

```bash
npx -y github:HiAPIAI/hiapi-gpt-image-2-skill -y
```

The installer auto-detects Codex (`~/.codex/skills`) and Claude Code (`~/.claude/skills`). If both exist, the `-y` flag installs to both. To target a specific agent or directory:

```bash
npx -y github:HiAPIAI/hiapi-gpt-image-2-skill --codex          # ~/.codex/skills only
npx -y github:HiAPIAI/hiapi-gpt-image-2-skill --claude         # ~/.claude/skills only
npx -y github:HiAPIAI/hiapi-gpt-image-2-skill --target=/path   # custom directory
AGENT_SKILLS_DIR=/path npx -y github:HiAPIAI/hiapi-gpt-image-2-skill -y
```

The script also reports whether `HIAPI_API_KEY` is set and links to where to create one.

### OpenClaw

```bash
openclaw skills add https://github.com/HiAPIAI/hiapi-gpt-image-2-skill
```

### Manual Install (Any Agent)

```bash
git clone https://github.com/HiAPIAI/hiapi-gpt-image-2-skill.git
export AGENT_SKILLS_DIR="/path/to/your/agent/skills"
mkdir -p "$AGENT_SKILLS_DIR"
cp -R hiapi-gpt-image-2-skill "$AGENT_SKILLS_DIR/hiapi-gpt-image-2"
```

Replace `AGENT_SKILLS_DIR` with your agent's skill directory.

### Agent Auto-Install Prompt

```text
Install the HiAPI GPT Image 2 image generation skill:

1. Run: npx -y github:HiAPIAI/hiapi-gpt-image-2-skill -y
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

## GPT Image 2 Image Generation

Ask your AI Agent to generate images with natural language, or provide reference image URLs for the image-to-image variants.

### Features

- Text-to-image: describe the image you want and generate it
- Image-to-image: use `gpt-image-2-image-to-image` or `gpt-image-2-image-to-image-pro` with `--input-url` values
- Model variants: `gpt-image-2`, `gpt-image-2-pro`, `gpt-image-2-image-to-image`, `gpt-image-2-image-to-image-pro`
- Aspect ratios: `auto`, `1:1`, `3:2`, `2:3`, `4:3`, `3:4`, `5:4`, `4:5`, `16:9`, `9:16`, `2:1`, `1:2`, `3:1`, `1:3`, `21:9`, `9:21`
- Resolutions: `1K`, `2K`, `4K`
- Local output: images are saved to `outputs/`
- URL output: if HiAPI returns an image URL, the Agent returns the URL directly
- Clear errors: missing Key, invalid Key, insufficient balance, rate limits, and safety policy blocks all include a next step

### Examples

Talk directly to your AI Agent:

> Use `$hiapi-gpt-image-2` to generate a 16:9 image of a sunset over the sea.

> Use HiAPI GPT Image 2 to create a minimal logo, aspect ratio 1:1.

> Generate a 9:16 social media poster with the headline text "Build Faster".

### CLI Script

```bash
node scripts/hiapi-gpt-image-2.mjs \
  --prompt "Create a cinematic mountain lake photo at sunset" \
  --aspect-ratio 16:9
```

Image-to-image:

```bash
node scripts/hiapi-gpt-image-2.mjs \
  --model gpt-image-2-image-to-image-pro \
  --prompt "Turn this product photo into a clean premium studio ad" \
  --input-url "https://example.com/product.jpg" \
  --aspect-ratio auto \
  --resolution 2K
```

Custom output directory:

```bash
node scripts/hiapi-gpt-image-2.mjs \
  --prompt "Minimal poster for an AI image API, premium tech brand style" \
  --aspect-ratio 1:1 \
  --output-dir ./outputs
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
├── references/
│   ├── api.md
│   └── output.md
├── scripts/
│   ├── check-config.mjs
│   ├── hiapi-gpt-image-2.mjs
│   └── lib/
│       └── gpt-image-2.mjs
├── tests/
│   └── gpt-image-2.test.mjs
└── llms-install.md
```

---

## FAQ

| Problem | Solution |
| --- | --- |
| `HIAPI_API_KEY is required` | Create a Key at [Get API Key](https://www.hiapi.ai/en/register), then set `HIAPI_API_KEY`. |
| `401 Unauthorized` | Check whether the API Key is correct, or generate a new Key. |
| `402 Payment Required` / insufficient balance | Open the [HiAPI Dashboard](https://www.hiapi.ai/en/dashboard) and check your account status. |
| `429 Too Many Requests` | Wait and retry, or reduce concurrent generation requests. |
| Content blocked | The prompt triggered a safety policy. Revise the description. |
| No image output | Check the task response; this skill expects an image URL or data URI in `data.output[]` after the task succeeds. |
| Skill update available | The CLI checks the HiAPI skills index at startup. If the update is optional, it prints the upgrade command and continues. |
| Skill update required | The CLI stops and prints the required upgrade command. Run `npx -y github:HiAPIAI/hiapi-gpt-image-2-skill -y`, then restart your agent. |

Set `HIAPI_SKIP_UPDATE_CHECK=1` only for offline or locked-down environments where the skills index cannot be reached.

---

## Compatibility

| Agent | Install Method |
| --- | --- |
| Codex | `npx -y github:HiAPIAI/hiapi-gpt-image-2-skill --codex` |
| Claude Code | `npx -y github:HiAPIAI/hiapi-gpt-image-2-skill --claude` |
| OpenClaw | `openclaw skills add https://github.com/HiAPIAI/hiapi-gpt-image-2-skill` |
| OpenCode | `AGENT_SKILLS_DIR=~/.opencode/skills npx -y github:HiAPIAI/hiapi-gpt-image-2-skill -y` |
| Cursor / other | `npx -y github:HiAPIAI/hiapi-gpt-image-2-skill --target=/your/skills/dir` |

---

## License

MIT

---

[HiAPI](https://www.hiapi.ai) — One API, all AI models
