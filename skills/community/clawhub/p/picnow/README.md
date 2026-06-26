# picnow — Image Generation Skill

> Generate images from any SKILL.md-compatible AI agent — text-to-image, image-to-image, 1K / 2K / 4K, powered by GPT-Image-2.

**Install & docs:** https://picnow.letmego.top/skills

---

## Quick start

### 1. Install

```bash
# skillpm — installs from npm
npx skillpm install @jxai/picnow

# skills — installs from GitHub
npx skills install jeekchen/picnow-skill

# SkillHub
skillhub install @jxai/picnow

# ClawHub
clawdhub install @jxai/picnow

# Manual
git clone https://github.com/jeekchen/picnow-skill
cp -r picnow-skill/skills/picnow ~/.claude/skills/picnow
```

### 2. Get a token (令牌)

Sign up at **https://api.letmego.top** and copy your token, then:

```bash
# macOS / Linux — add to ~/.zshrc or ~/.bashrc to persist
export LETMEGO_API_KEY=your_token

# Windows PowerShell (permanent)
[System.Environment]::SetEnvironmentVariable("LETMEGO_API_KEY","your_token","User")
```

### 3. Use it

Just talk to your agent — the skill activates automatically:

```
> 帮我画一张珠宝产品主图，白色背景，高清
> Generate a landscape banner for a coffee brand
> 把这张图改成动漫风格  [attach reference.jpg]
> Create a portrait poster for a music festival
```

---

## Parameters

| Parameter | Options | Default |
|-----------|---------|---------|
| `--prompt` | Any text | *(required)* |
| `--quality` | `1k` · `2k` · `4k` | `1k` |
| `--aspect` | `square` · `landscape` · `portrait` | `square` |
| `--n` | 1 – 10 | `1` |
| `--ref` | Local image path | *(none → text-to-image)* |

**Quality guide**

| Quality | Max resolution | Best for |
|---------|---------------|----------|
| `1k` | 1536 × 1536 | Previews, social media |
| `2k` | 2048 × 2048 | E-commerce, print |
| `4k` | 3840 × 2160 | Landscape / portrait only |

---

## Direct script usage

```bash
# Text-to-image
LETMEGO_API_KEY=your_token node skills/picnow/scripts/generate.js \
  --prompt "product photo, white background, studio lighting" \
  --quality 2k --aspect square --n 1

# Image-to-image (style transfer / edit)
LETMEGO_API_KEY=your_token node skills/picnow/scripts/generate.js \
  --prompt "anime style, vibrant colors" \
  --quality 1k --aspect square --ref ./reference.jpg
```

Output: a single JSON line — `{ "urls": ["https://..."] }`

---

## Supported clients

- **Claude Code** (via `npx skillpm` or manual install)
- **OpenAI Codex CLI**
- **OpenClaw**
- Any agent that supports the SKILL.md standard

---

## Published on

- [SkillsMP](https://skillsmp.com)
- [ClawHub](https://clawhub.ai)
- [SkillHub](https://skillhub.club)

---

## License

MIT © [jeekchen](https://github.com/jeekchen)
