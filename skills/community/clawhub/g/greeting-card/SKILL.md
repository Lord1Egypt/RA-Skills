---
name: greeting-card
description: Generate beautiful greeting cards for various occasions (birthday, holiday, encouragement, apology, etc.). Use when the user asks to create a greeting card, write wishes, or compose messages for someone. Supports Chinese and English, multiple tones (warm, funny, formal), and different card styles.
---

# Greeting Card Generator

When the user asks you to create a greeting card:

1. **Ask who it's for** (friend, family, colleague, partner?)
2. **Ask the occasion** (birthday, new year, graduation, apology, get well, thank you, encouragement, etc.)
3. **Ask preferred tone** (warm hearted, funny, formal, poetic, simple)
4. **Ask preferred language** (Chinese, English, or bilingual)

## Default Format

Generate cards in a **clean, social-media-friendly format** — no ASCII borders.
Surround emoji, short lines, easy to copy-paste to WeChat / Moments / WhatsApp.

Template:
```
[Title emoji] [Title] [Title emoji]

[Message body - 祝福语正文]

[Sender's name / closing line]

[Decorative touch emoji]
```

## Examples by Occasion

### Birthday (Warm - Chinese)
```
🎂 生日快乐 🎂

又一年，世界又见证了你多了一岁
的可爱。愿你新的一岁里：

有吃不完的好吃的
有做不完的美梦
有发不完的财（这个很重要）

最重要的——天天开心！

── 爱你的 XX

🎉 今天你最大！
```

### Encouragement (Warm - English)
```
🌟 You Got This 🌟

Remember why you started.

The road is tough,
but so are you.

One step at a time.
You're closer than
you think.

── Your cheerleader

💪 Keep going!
```

### Birthday (Funny - Chinese)
```
🎉 恭喜你又老了一岁！🎉

经检测，你的年龄新鲜度：
████████████████░░  87%
还能再撑好几年！

生日愿望清单：
☐ 变瘦（算了）
☐ 变富（努力中）
☑ 变得比你帅（已达成）

── 你的损友 XX

🥳 蛋糕分我一块！
```

## Format Rules

- **No ASCII borders** — output should be clean text, ready to copy-paste to chat apps
- Use emoji decorations on their own lines (not inside boxes)
- Keep line lengths moderate for mobile screen readability
- Separate sections with blank lines
- Title + emoji on first line, then blank line, then body

## Tips for Better Cards

- Match decorations (emoji/emoji sequences) to occasion
- Keep message length appropriate for relationship
- Add personal details the user mentions
- Bilingual cards when the recipient uses both languages
- Suggest adding a real photo or drawing to the card
- If the user has no preference, default to warm + Chinese

## Relationship Tone Guide

| Relationship | Best Tone |
|-------------|-----------|
| Partner / Spouse | Warm, romantic, personal |
| Parent / Family | Warm, respectful |
| Close friend | Warm or funny |
| Colleague / Boss | Formal or warm (not funny) |
| Teacher | Formal, respectful |
| Child | Playful, warm, simple words |
