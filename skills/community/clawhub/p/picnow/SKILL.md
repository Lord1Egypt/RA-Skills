---
name: picnow
description: >
  Generate high-quality images via Picnow (api.letmego.top). Activate when
  the user wants to create, generate, draw, or design images — including
  product photos, posters, banners, illustrations, social media visuals,
  hero shots, covers, and thumbnails. Also handles image editing: style
  transfer, background change, image-to-image (改图/配图/修图/图改图).
  Supports 1K / 2K / 4K resolution, square / landscape / portrait aspect ratios.
  Requires LETMEGO_API_KEY environment variable (your letmego 令牌/token).
when_to_use:
  # English triggers
  - User asks to generate, draw, create, or make an image / picture / photo / visual / graphic / artwork / illustration
  - User says "image for", "picture for", "visual for", "banner for", "poster for"
  - User wants a product photo, hero shot, thumbnail, cover, poster, banner, or social media image
  - User wants to edit, retouch, restyle, stylize, or transform an existing image
  - User wants image-to-image, style transfer, background change, or outpainting
  - User asks to "add an image", "pair with image", "create a graphic", or "design a visual"
  - User wants to render, visualize, or illustrate something
  # 中文触发词
  - 用户说 生图 / 出图 / 做图 / 画图 / 画张 / 画一张 / 帮我画 / 帮我出图
  - 用户说 配图 / 加图 / 插图 / 来张图 / 给我图 / 图片素材
  - 用户说 改图 / 修图 / 图改图 / 换风格 / 风格化 / 重绘
  - 用户说 生成图片 / 生成图像 / 创作图 / 设计图
  - 用户说 产品图 / 主图 / 效果图 / 宣传图 / 海报 / 封面 / 头图 / 背景图
  - 用户说 换背景 / 去背景 / 修改图片 / 图片编辑
allowed-tools:
  - Bash
---

# Picnow Image Generation Skill

Picnow wraps the `api.letmego.top` GPT-Image-2 API. This skill handles
text-to-image and image-to-image (edit) generation.

The script uses the **async API** (`/v1/async/images/...`) — it submits the
job, polls until completion, and prints the final URL. This avoids the 100s
Cloudflare edge timeout that 2K/4K renders used to hit. A single call may
take up to ~5 minutes for heavy renders; no extra flags needed.

## 1. Environment check

Before generating, verify the token is set:

```bash
if [ -z "$LETMEGO_API_KEY" ]; then
  echo "❌ LETMEGO_API_KEY is not set."
  echo "Visit https://api.letmego.top to get your 令牌, then:"
  echo "  export LETMEGO_API_KEY=your_token"
  exit 1
fi
```

## 2. Gather parameters

Ask the user if not already provided:

| Parameter | Options | Default |
|-----------|---------|---------|
| `prompt` | any text description | *(required)* |
| `quality` | `1k` · `2k` · `4k` | `1k` |
| `aspect` | `square` · `landscape` · `portrait` | `square` |
| `n` | 1 – 10 | `1` |
| `ref` | local file path (optional) | *(none → text-to-image)* |

**Quality guide:**
- `1k` — up to 1536×1536, fast and cheap, great for previews and social media
- `2k` — up to 2048×2048, suitable for e-commerce and print
- `4k` — up to 3840×2160, landscape or portrait only (no 4k square)

## 3. Locate and run the generation script

```bash
# Resolve skill directory (user-global → project-local)
SKILL_DIR="$HOME/.claude/skills/picnow"
[ -d "$SKILL_DIR" ] || SKILL_DIR=".claude/skills/picnow"

node "$SKILL_DIR/scripts/generate.js" \
  --prompt "PROMPT_HERE" \
  --quality QUALITY \
  --aspect ASPECT \
  --n N
  # add: --ref /path/to/image.jpg   for image-to-image
```

The script outputs a single JSON line:
```json
{ "urls": ["https://...cdn.../image.png"] }
```

## 4. Present results

- Display each URL as a clickable link or inline image.
- For multiple images, list them with index labels (1/3, 2/3, …).
- Offer to download, save to a project, or run another variation.

## Error handling

| Exit condition | Meaning | Action |
|---|---|---|
| `LETMEGO_API_KEY` missing | Token not set | Guide user to picnow settings |
| HTTP 401 | Token invalid | Ask user to check or refresh token |
| HTTP 402 / quota | Insufficient balance | Direct to letmego.top recharge |
| HTTP 4xx other | Bad request | Show upstream error message |
| Network error | Connection issue | Suggest retry |

## Examples

**Text-to-image:**
```
User: 帮我画一张珠宝产品主图，白色背景，高清
→ quality=2k, aspect=square
→ node "$SKILL_DIR/scripts/generate.js" \
    --prompt "jewelry product hero shot, white background, studio lighting, photorealistic" \
    --quality 2k --aspect square --n 1
```

**Image-to-image:**
```
User: 把这张图改成动漫风格 [uploads reference.jpg]
→ quality=1k, ref=reference.jpg
→ node "$SKILL_DIR/scripts/generate.js" \
    --prompt "anime style illustration, vibrant colors, clean linework" \
    --quality 1k --aspect square --n 1 --ref reference.jpg
```

**Landscape banner:**
```
User: Generate a landscape banner for a coffee brand
→ quality=1k, aspect=landscape, n=2
→ node "$SKILL_DIR/scripts/generate.js" \
    --prompt "coffee brand lifestyle banner, warm tones, morning light, artisan aesthetic" \
    --quality 1k --aspect landscape --n 2
```
