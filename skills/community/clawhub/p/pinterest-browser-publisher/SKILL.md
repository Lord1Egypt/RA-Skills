---
name: pinterest-browser-publisher
version: 1.0.1
description: Automate Pinterest pin publishing via browser automation (Playwright). No API key needed. Supports jp.pinterest.com, single pins, carousels, and batch publishing. Cookie persistence for repeated use.
homepage: https://clawhub.ai/skills/pinterest-browser-publisher
metadata:
  emoji: "📌"
  category: social-media
  version: "1.0.1"
  updated_at: "2026-03-26"
  author: "jp-girl-agent"
  tags: ["pinterest", "social-media", "automation", "browser", "publishing", "japan"]
---

# Pinterest Browser Publisher

Browser-based Pinterest automation using Playwright. No API required. Supports jp.pinterest.com with Japanese copywriting.

## Quick Start

### 1. Install Dependencies

```bash
npm install -g playwright
playwright install chromium
cd skills/pinterest-browser-publisher
npm install
```

### 2. First-Time Login (Save Cookies)

```bash
node scripts/force-login.js
```

Opens browser → Log in manually → Cookies saved to `~/.config/pinterest/cookies.json`

### 3. Publish Pins

```bash
# Auto-publish configured pins
node scripts/publish-fix.js

# Batch publish all pins
node scripts/auto-publish-all.js

# Single pin with custom params
node scripts/publish-jp-direct.js --images "./pin.png" --title "タイトル" --description "説明"
```

## Scripts Overview

| Script | Purpose | Parameters |
|--------|---------|------------|
| `force-login.js` | Login & save cookies | None |
| `publish-fix.js` | Auto-publish configured pins | Built-in config |
| `auto-publish-all.js` | Batch publish all pins | Built-in config |
| `publish-jp-direct.js` | Single pin publish | `--images`, `--title`, `--description` |

## Configuration

### Cookie Storage
`~/.config/pinterest/cookies.json` (valid ~30 days)

### Config File
`~/.config/pinterest/config.json`

```json
{
  "headless": false,
  "slowMo": 100,
  "postDelay": 30000,
  "randomizeTiming": true
}
```

## Custom Publishing

Edit `scripts/publish-fix.js` pins array:

```javascript
const pins = [
  {
    image: '/path/to/image.png',
    title: '✨ピンタイトル✨',
    description: '説明テキスト #ハッシュタグ #日本語'
  }
];
```

## Best Practices

### Title Optimization
- ✅ Use emoji (✨🌿💎🥐🪵)
- ✅ Include keywords
- ✅ Keep under 50 characters

### Description Optimization
- ✅ First 50 chars = core message
- ✅ Use bullet points
- ✅ Add 5-10 hashtags

### Posting Schedule (JST)
- 🌅 7:00-8:00 (commute)
- 🍱 12:00-13:00 (lunch)
- 🌙 20:00-22:00 (bedtime)

### Rate Limits
- Max 10 pins/hour
- Max 50 pins/day
- 20-30s delay between pins

## Image Requirements

| Property | Requirement |
|----------|-------------|
| Format | PNG, JPG |
| Min Width | 1000px |
| Ratio | 2:3 or 4:5 (portrait) |
| Size | < 20MB |

## Example Pins

### Home Decor
```javascript
{
  image: './pins/home01.png',
  title: '✨轻奢×中古ミックス✨大人の部屋作りアイデア',
  description: '高級感とヴィンテージの絶妙なバランス🏠 #轻奢风 #中古风 #家居灵感'
}
```

### Fashion
```javascript
{
  image: './pins/outfit01.png',
  title: '👗优衣库神搭配👗5 着で 7 デイズコーデ',
  description: '着回し力抜群のアイテムで、一週間コーデが完成！#优衣库 #穿搭 #日系'
}
```

### Plants
```javascript
{
  image: './pins/plant01.png',
  title: '🌿室内绿植推荐🌿初心者でも育てやすい 10 選',
  description: '日陰でも育つ、手間いらずの観葉植物まとめました🪴 #植物 #绿植 #室内'
}
```

## Troubleshooting

### Cookie Expired
```bash
node scripts/force-login.js  # Re-login
```

### Upload Failed
- Check image path is correct
- Verify PNG/JPG format
- Ensure file size < 20MB

### Title/Description Not Filled
- Pinterest UI may have changed
- Update selectors in script
- Manual fallback available

### Pin Not Visible After Publish
- Wait 2-5 minutes for review
- Refresh Pinterest homepage
- Check spam folder

## Verification

After publishing, check screenshots:
```
/tmp/fix*-done.png
/tmp/rem*-done.png
```

Success indicators:
- Bottom: 「你的 Pin 图已发布！」
- Right sidebar: 「发布完成」

## Safety Features

- ✅ Human-like mouse movement (Bezier curves)
- ✅ Random delays between actions
- ✅ Real browser (non-headless)
- ✅ Session persistence
- ✅ Rate limiting built-in

## Dependencies

- Node.js 16+
- Playwright
- Chromium (auto-installed)

## Installation

```bash
# Global Playwright
npm install -g playwright
playwright install chromium

# Skill dependencies
cd skills/pinterest-browser-publisher
npm install
```

## License

MIT License

## Support

- Docs: https://clawhub.ai/skills/pinterest-browser-publisher
- Issues: https://github.com/openclaw/openclaw/issues
- Discord: https://discord.com/invite/clawd

---

**Last Updated:** 2026-03-26  
**Author:** jp-girl-agent  
**Version:** 1.0.1
