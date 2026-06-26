---
name: nano-banana2-apiyi
description: Generate images via APIYI (Gemini 3.1 Flash Image Preview). Use when user wants to generate images from text descriptions. Supports keyword extraction, prompt restructuring, and direct image generation.
metadata:
  {
    "openclaw":
      {
        "emoji": "🍌",
        "requires": { "bins": ["python3"], "env": ["APIYI_API_KEY"] },
        "primaryEnv": "APIYI_API_KEY",
      },
  }
---

# Nano Banana 2 (APIYI)

Generate images from text descriptions using APIYI's Gemini 3.1 Flash Image Preview API.

## Quick Start

当用户说“生成一张xxx图片 / 帮我生成xxx”时，**必须先走中文提示词选择流程**（先给选择、再生成；此阶段绝不调用生成 API）：

1) 先调用脚本候选输出（不生成）：
   - `python {baseDir}/scripts/generate_image.py --suggest-zh "<用户需求>"`
   - 把返回的 A/B/C 三套“增强中文提示词 + 反向词”发给用户让其选择
2) 用户选择 A/B/C
   - 若用户选择 A（北欧极简方向），再调用：
     `python {baseDir}/scripts/generate_image.py --suggest-zh-a "<用户需求>"`
     并把 A1/A2/A3 发给用户二次选择
3) 用户最终确认：版本（A/B/C 或 A1/A2/A3）+ 比例（16:9/9:16/1:1）+ 清晰度（1K/2K）
4) **仅在用户确认后**，才调用生成脚本：
   - `python {baseDir}/scripts/generate_image.py --prompt "<最终提示词>" --aspect-ratio "<比例>" --size "<1K/2K>"`

> 说明：APIYI 对英文更友好；如用户追求更稳定/更像参考图，可在第 4 步把“最终中文提示词”再改写为英文 prompt 后生成。

## 中文提示词候选（不生成，只给选择）

A/B/C 三选一：

```bash
python {baseDir}/scripts/generate_image.py --suggest-zh "简约独居冷色治愈"
```

若用户选 A（北欧极简方向），再给 A1/A2/A3：

```bash
python {baseDir}/scripts/generate_image.py --suggest-zh-a "简约独居冷色治愈"
```

## Basic Generation

```bash
python {baseDir}/scripts/generate_image.py --prompt "你的最终提示词" --filename "output.png" --aspect-ratio "16:9" --size "2K"
```

## Advanced: Prompt Restructuring Workflow

For better results, restructure user description into optimized prompts:

### Step 1: Understand User Input
Extract from user's description:
- **Subject**: What object/person/scene
- **Style**: Illustration, realistic, watercolor, oil painting, minimal, tech, Japanese, Chinese retro, etc.
- **Mood/Atmosphere**: Warm, cold, nostalgic, futuristic, cozy, etc.
- **Technical**: HD, detailed, close-up, bokeh, etc.

### Step 2: Restructure Prompt
Combine elements into English prompt:

Template:
```
[Subject], [Style], [Mood/Atmosphere], [Lighting], [Material], [Composition], [Technical params]
```

Example:
- User: "一只可爱的柴犬坐在樱花树下，水彩画风格，高清细节"
- Restructured: "A cute柴犬 sitting under a cherry blossom tree, watercolor painting style, soft pastel colors, delicate details, HD quality, illustration aesthetic"

### Step 3: Generate

```bash
python3 {baseDir}/scripts/generate_image.py \
  --prompt "A cute dog sitting under cherry blossoms, watercolor style, soft pastel colors, spring atmosphere, HD quality" \
  --filename "2026-03-12-16-00-00-sakura-dog.png" \
  --aspect-ratio "16:9" \
  --size "2K"
```

## Parameters

| Parameter | Options | Default |
|-----------|---------|---------|
| `--aspect-ratio` | `1:1`, `16:9`, `9:16` | `16:9` |
| `--size` | `1K`, `2K` | `2K` |

## API Key Configuration

Set in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "nano-banana2-apiyi": {
      "apiKey": "sk-your-api-key"
    }
  }
}
```

Or use `--api-key` flag directly.

## Examples

### Example 1: Tech Poster
User: "生成一张科技感的数据可视化海报"

Restructured: "Data visualization dashboard with futuristic UI, neon blue and purple color scheme, holographic interface, clean lines, tech poster style, high definition"

### Example 2: Vintage Photography
User: "生成一张复古胶片风格的咖啡店照片"

Restructured: "Cozy coffee shop interior, vintage film photography style, warm golden lighting, analog film grain, nostalgic atmosphere, 35mm film look, detailed"

### Example 3: Product Shot
User: "帮我生成一个简约的香水瓶商业摄影"

Restructured: "Elegant perfume bottle on clean background, commercial product photography, minimalist style, soft studio lighting, luxury branding, high-end packaging, professional advertising photo"

## Notes

- Always use English prompts for better APIYI performance
- Use timestamps in filenames: `yyyy-mm-dd-hh-mm-ss-name.png`
- The script prints `MEDIA:` line for auto-attach on supported chat providers
- Do not read the image back; report the saved path only
