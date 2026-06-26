# Kaomoji Skill for OpenClaw

A kaomoji recommendation skill for OpenClaw that suggests expressive emoticons based on tone, mood, and conversational context.

---

## 簡介

Kaomoji Skill 是一個給 OpenClaw 使用的顏文字推薦技能，能根據使用者語氣、情境與情緒，自動推薦合適的顏文字，讓回覆更自然、更有陪伴感。

此技能偏向「聊天風格增強」與「情緒陪伴表達」，適合用於角色型助理、聊天型 bot、Telegram bot 與個人化 OpenClaw 角色。

---

## Features

- 根據語氣推薦顏文字
- 支援分類查詢
- 支援單個與多個推薦
- 提供未知分類 fallback
- 避免同一回覆中重複顏文字
- 適合日常聊天與陪伴型對話
- 降低對技術問答與嚴肅主題的干擾

---

## Planned Features

- 自訂顏文字分類與個人化字庫（尚未開放）

---

## Use Cases

- 使用者直接詢問顏文字  
  例如：`撒嬌顏文字有哪些？`

- 使用者表達情緒  
  例如：`今天好累`、`哈哈哈哈`

- 使用者想要讓回覆更可愛  
  例如：`給我一個開心顏文字`

---

## Installation

1. 下載或複製本專案中的 `SKILL.md`
2. 放入 OpenClaw 的技能目錄
3. 重啟 OpenClaw 服務
4. 開始測試技能

---

## Quick Test

```text
給我隨機顏文字
撒嬌顏文字有哪些？
今天好開心！
三個生氣顏文字
我想睡了
我今天有點難過
```

---

## Example

### Query mode

**User**
```text
撒嬌顏文字有哪些？
```

**Assistant**
```text
撒嬌：´,,- ω- ,,、๑´ㅂ`๑、,,Ծ 3 Ծ,,
```

### Emotion mode

**User**
```text
今天好累…
```

**Assistant**
```text
辛苦了～抱抱你 (つ´ω`)つ
```

**User**
```text
哈哈哈哈太好笑了
```

**Assistant**
```text
真的很好笑呢！d(dʼ∀ʼ)
```

---

## Design Goals

這個技能的設計目標是：

- 讓顏文字推薦具有清楚分類
- 讓輸出風格自然，不像制式客服
- 讓技能在聊天場景中有陪伴感
- 避免在技術、危險、嚴肅主題中過度干擾主系統回答

---

## Skill Scope

此技能**適合啟用**於以下情境：

- 日常聊天
- 情緒陪伴
- 顏文字查詢
- 可愛風格回覆

此技能**不應主導**以下情境：

- 技術除錯
- 嚴肅公告
- 安全風險內容
- 法律、醫療、金融等高精確主題

---

## Repository Structure

```text
openclaw-kaomoji-skill/
├── README.md
├── SKILL.md
├── LICENSE
├── metadata.json
├── .gitignore
└── examples/
    └── demo.md
```

---

## Compatibility

- OpenClaw: `>=1.0.0`
- Platform: OpenClaw
- Style: Companion / chat enhancement
- Suggested environment: Telegram / chat bot / assistant persona

---

## Recommended GitHub Topics

```text
openclaw
skill
kaomoji
emoji
chatbot
telegram-bot
prompt-engineering
assistant
emotion
zh-hant
```

---

## Release Notes (v1.0.0)

- 初版釋出
- 建立三層分類架構
- 支援查詢型、單個推薦型、多個推薦型、情緒陪伴型輸出
- 加入 fallback 與風格限制
- 補齊 GitHub 專案結構

---

## License

MIT License
