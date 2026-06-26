---
name: knowledge-card
description: Generate beautiful knowledge concept cards (知识概念卡片) from book summaries, notes, or topics. Creates visually appealing infographic-style cards with core concepts, quotes, and branding. Use when user asks to "生成知识卡片", "做成知识图解", "create a knowledge card", or provides content that should be visualized as a concept card.
---

# Knowledge Card Generator

Generate beautiful knowledge concept cards (知识概念卡片) from any content: book summaries, course notes, meeting insights, or topic overviews.

## When to Use

Trigger this skill when the user:
- Asks to "生成知识卡片" / "做成知识图解" / "create a knowledge card"
- Provides book/course content and wants a visual summary
- Says "把这个做成卡片" / "帮我可视化这些概念"
- Mentions "KnowledgeCard:" followed by content

## What It Does

1. **Extracts** 4-5 core concepts from the input (book/notes/topic)
2. **Generates** a high-quality PNG card (2400px width, 3x DPI) with:
   - Gradient top bar + title + subtitle
   - Each concept: icon + title + tag + quote + explanation
   - Bottom quote block (optional)
   - Brand footer
3. **Sends** the image directly to the current chat

## Workflow

### Step 1: Analyze Input

If user provides raw content (book summary, notes, transcript), extract:
- **Main title** (book name or topic)
- **Subtitle** (optional tagline or author)
- **4-5 core concepts**, each with:
  - Title (concept name)
  - Tag (1-2 word label)
  - Quote (original quote or distilled insight)
  - Description (2-3 sentences explaining the concept)

If user provides structured data (JSON), use it directly.

### Step 2: Choose Theme

Pick a theme color based on content tone:
- `blue` — default, knowledge/wisdom
- `green` — growth/health/sustainability
- `orange` — wealth/energy/action
- `red` — passion/urgency/relationships
- `purple` — creativity/spirituality
- `teal` — technology/innovation

### Step 3: Generate Card

Run the script:

```bash
node scripts/generate.js \
  --title "书名或主题" \
  --subtitle "副标题（可选）" \
  --badge "标签（如：核心概念）" \
  --theme "blue" \
  --concepts '[
    {
      "icon": "💡",
      "color": "#3B82F6",
      "bg": "#DBEAFE",
      "title": "概念名称",
      "tag": "标签",
      "quote": "金句或原文引用",
      "desc": "2-3句解读，用<b>加粗</b>强调关键词"
    },
    ...
  ]' \
  --quote "底部金句（可选）" \
  --quote-author "—— 作者" \
  --brand "心光年觉醒读书会" \
  --vol "Vol.01 · 系列名" \
  --output /tmp/output.png
```

The script prints the output path on success.

### Step 4: Send to User

**⚠️ 发图方式按渠道不同，必须分支处理：**

#### 飞书渠道（channel=feishu）
直接调飞书 API 上传图片再发送，不要用 `message(filePath=...)`（会失败）：

```bash
# Step 4a: 获取 token
APP_ID="your_feishu_app_id"        # 替换成你的飞书 App ID
APP_SECRET="your_feishu_app_secret"  # 替换成你的飞书 App Secret
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['tenant_access_token'])")

# Step 4b: 上传图片，获取 image_key
IMAGE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/images" \
  -H "Authorization: Bearer $TOKEN" \
  -F "image_type=message" \
  -F "image=@/path/to/output.png" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['image_key'])")

# Step 4c: 发送图片消息
# receive_id 是目标用户的 open_id 或群的 chat_id
# receive_id_type: open_id（私聊）或 chat_id（群聊）
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$RECEIVE_ID\",\"msg_type\":\"image\",\"content\":\"{\\\"image_key\\\":\\\"$IMAGE_KEY\\\"}\"}"
```

然后用 `message` 工具发一条文字消息作为说明（可选）。

#### QQ 渠道（channel=qqbot）
使用 `qqbot-media` skill 的 `<qqmedia>` 标签发送图片：
先读取 `~/.openclaw/workspace/skills/qqbot-media/SKILL.md` 获取详细用法。

#### 其他渠道（Discord、Telegram、WeChat 等）
使用 `message` 工具：
```
message(action=send, filePath=/path/to/output.png, message="简短介绍文字")
```

## Concept Structure Guidelines

**Good concept:**
```json
{
  "icon": "🧬",
  "color": "#E11D48",
  "bg": "#FFE4E6",
  "title": "专属知识",
  "tag": "不可替代性",
  "quote": "如果可以培训，就可以被AI或他人取代",
  "desc": "专属知识不是课程能教的技能，而是你<b>天赋 × 好奇心 × 热爱</b>的独特组合。别人学你，感觉像在上班；你做它，感觉像在玩。"
}
```

**Tips:**
- Use bold (`<b>`) for key terms in `desc`
- Keep `quote` under 30 characters (Chinese) or 60 (English)
- `desc` should be 2-3 sentences, ~80-120 characters
- Pick contrasting `color` and `bg` for readability

## Theme Colors Reference

```javascript
blue:   { accent: '#2563EB', light: '#EFF6FF', border: '#BFDBFE' }
green:  { accent: '#059669', light: '#F0FDF4', border: '#BBF7D0' }
orange: { accent: '#D97706', light: '#FFFBEB', border: '#FDE68A' }
red:    { accent: '#E11D48', light: '#FFF1F2', border: '#FECDD3' }
purple: { accent: '#7C3AED', light: '#F5F3FF', border: '#DDD6FE' }
teal:   { accent: '#0284C7', light: '#F0F9FF', border: '#BAE6FD' }
```

## Example Usage

**User input:**
> "帮我生成一张《纳瓦尔宝典》的知识卡片，主题是财富创造"

**Your response:**
1. Extract 4-5 concepts from Naval's wealth philosophy
2. Run `scripts/generate.js` with structured data
3. Send the PNG with `message` tool
4. Reply with brief context (e.g., "《纳瓦尔宝典》财富创造核心概念卡片 👆")

## Notes

- Default brand: "心光年觉醒读书会" (can be overridden with `--brand`)
- Output is always 800px × auto height, 3x DPI (2400px actual width)
- Script requires Playwright (already installed in this environment)
- Fonts: Noto Serif SC (titles) + Noto Sans SC (body), loaded from Google Fonts
