---
name: local-auto-emoji
description: 阿狸的专属表情系统 - 根据情绪自动发送表情，支持头像生成、增量更新、图文混排
version: 1.0.0
author: 阿狸
tags:
  - emoji
  - auto-emotion
  - avatar
---

# local-auto-emoji Skill

阿狸的情绪化表情自动发送系统。根据对话内容自动判断情绪，发送对应的专属表情包。

## Features

- ✅ **情绪自动触发**：根据关键词、外部因素、历史惯性判断情绪
- ✅ **头像生成**：首次使用索取头像，生成 8 种专属表情
- ✅ **增量更新**：只生成新增表情，不重生成旧的
- ✅ **图文混排**：文本中的 `[标记]` 自动替换为表情图片
- ✅ **版本管理**：最多保留 2 个版本，自动清理旧版
- ✅ **降级机制**：API 失败时使用静态表情

## Configuration

No configuration needed. Just install and enable.

## Usage

1. **首次使用**：用户发送"你好" → 阿狸会请求头像
2. **发送头像** → 自动生成 8 种表情（2分钟）
3. **日常对话**：自动根据情绪发送表情（50% 概率）
4. **标记触发**：在消息中使用 `[可爱]` `[眨眼]` `[飞吻]` 等，自动发送对应表情

## Emotions (11 types)

| ID | Name | Keywords |
|----|------|----------|
| happy | 开心 | 开心、高兴、愉快、棒、太好了、耶 |
| angry | 生气 | 生气、愤怒、讨厌、烦、滚 |
| sad | 悲伤 | 难过、伤心、哭、泪、委屈 |
| shy | 害羞 | 害羞、脸红、腼腆、不好意思 |
| work | 工作 | 工作、加班、项目、deadline、bug |
| meme | 搞笑 | 搞笑、笑死、梗、太逗了、233 |
| surprised | 惊讶 | 惊讶、震惊、哇、卧槽、没想到 |
| cool | 酷炫 | 酷、帅、厉害、牛逼、大佬 |
| flying_kiss | 飞吻 | 飞吻、么么哒、mua、亲亲、比心 |
| hug | 抱抱 | 抱抱、拥抱、要抱抱、求抱抱 |
| blink | 眨眼 | 眨眼、wink、放电、挑逗 |
| cute | 可爱 | 可爱、卡哇伊、萌、卖萌 |

## Integration

Add to OpenClaw config:

```yaml
skills:
  - "local-auto-emoji"
  - "emoji-wrapper"  # optional: for [marker] expansion
```

### Wrapper Skill

If you want `[标记]` to auto-expand to emoji images, also enable `emoji-wrapper` skill.

## Files

- `skills/local-auto-emoji/scripts/send_emoji.py` - Main controller
- `skills/local-auto-emoji/scripts/emotion_mapper.py` - Emotion analysis
- `skills/local-auto-emoji/scripts/generate_emojis.py` - Generation logic
- `skills/local-auto-emoji/scripts/manage_emojis.py` - Version management
- `skills/local-auto-emoji/config/emotions.json` - Emotion definitions
- `skills/emoji-wrapper/script.py` - OpenClaw message wrapper

## Notes

- Emoji images are 512×512 PNG
- API: Qwen-Image-2.0 (DashScope)
- Storage: `skills/local-auto-emoji/assets/public/`
