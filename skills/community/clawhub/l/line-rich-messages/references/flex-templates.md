# LINE Flex Message Templates (Raw JSON)

Since OpenClaw directives (`[[tag: ...]]`) can sometimes fail depending on the environment, use these **Raw JSON** structures for 100% reliable rendering.

## 1. Interaction: Button Menu
**Scenario**: Main menu, feature selection, or delivering a download link.

```json
{
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      { "type": "text", "text": "標題名稱", "weight": "bold", "color": "#1DB446", "size": "sm" }
    ]
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      { "type": "text", "text": "這裡放置詳細的描述文字，支援自動換行。", "wrap": true, "size": "xs", "color": "#666666" }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "color": "#1DB446",
        "action": { "type": "message", "label": "回傳文字按鈕", "text": "指令內容" }
      },
      {
        "type": "button",
        "style": "link",
        "action": { "type": "uri", "label": "開啟連結按鈕", "uri": "https://..." }
      }
    ]
  }
}
```

## 2. Information: Structured Data (List)
**Scenario**: Displaying settings, status, or item lists.

```json
{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      { "type": "text", "text": "📊 狀態報告", "weight": "bold", "size": "md" },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              { "type": "text", "text": "項目一", "color": "#aaaaaa", "size": "sm", "flex": 2 },
              { "type": "text", "text": "🟢 正常", "wrap": true, "color": "#666666", "size": "sm", "flex": 5 }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              { "type": "text", "text": "項目二", "color": "#aaaaaa", "size": "sm", "flex": 2 },
              { "type": "text", "text": "內容描述", "wrap": true, "color": "#666666", "size": "sm", "flex": 5 }
            ]
          }
        ]
      }
    ]
  }
}
```

## 3. Quick Choice: Simple Confirm
**Scenario**: Yes/No decisions where a card is better than a system pop-up.

```json
{
  "type": "bubble",
  "size": "micro",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      { "type": "text", "text": "確認執行嗎？", "weight": "bold", "align": "center" },
      {
        "type": "box",
        "layout": "horizontal",
        "margin": "md",
        "contents": [
          { "type": "button", "action": { "type": "message", "label": "是", "text": "yes" } },
          { "type": "button", "action": { "type": "message", "label": "否", "text": "no" } }
        ]
      }
    ]
  }
}
```

## 4. Visual: Image Hero + CTA
**Scenario**: Covers for stories, featured announcements, or high-quality deliveries with an image.

```json
{
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://example.com/hero.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      { "type": "text", "text": "精選標題", "weight": "bold", "size": "xl" },
      { "type": "text", "text": "描述內容，引導使用者點擊下方按鈕。", "wrap": true, "size": "sm", "color": "#666666" }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "color": "#1DB446",
        "action": { "type": "uri", "label": "了解詳情", "uri": "https://..." }
      }
    ]
  }
}
```

## 5. Interaction: Quick Replies (Bubbles)
**Scenario**: Providing 2-13 floating bubbles at the bottom for quick choices without cluttering chat history.

```json
{
  "type": "text",
  "text": "請選擇妳的下一步：",
  "quickReply": {
    "items": [
      {
        "type": "action",
        "action": { "type": "message", "label": "選項一", "text": "執行一" }
      },
      {
        "type": "action",
        "action": { "type": "message", "label": "選項二", "text": "執行二" }
      }
    ]
  }
}
```
