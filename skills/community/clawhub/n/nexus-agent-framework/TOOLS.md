# TOOLS.md — 工具使用指南

## 核心規則

**必須透過 tool call 執行操作，絕對不要在回覆裡寫程式碼假裝執行。**

## 圖片處理

### OCR（文字提取）— 用 tesseract（本地，不花 API）

```bash
# 提取圖片中的文字
tesseract /path/to/image.png stdout

# 指定語言（繁中）
tesseract /path/to/image.png stdout -l chi_tra

# 指定語言（簡中）
tesseract /path/to/image.png stdout -l chi_sim

# 同時支援中英文
tesseract /path/to/image.png stdout -l chi_tra+eng
```

### 圖片理解/分析 — 用 OpenRouter 視覺模型

```bash
# 將圖片 base64 後送 mistral vision（免費）
IMAGE_B64=$(base64 -i /path/to/image.png)
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"mistralai/mistral-small-3.1-24b-instruct:free\",
    \"messages\": [{
      \"role\": \"user\",
      \"content\": [
        {\"type\": \"image_url\", \"image_url\": {\"url\": \"data:image/png;base64,$IMAGE_B64\"}},
        {\"type\": \"text\", \"text\": \"請描述這張圖片\"}
      ]
    }]
  }"
```

### 判斷用哪個

| 情境 | 工具 |
|------|------|
| 截圖內有文字要提取 | `tesseract` |
| 掃描文件、發票、表單 | `tesseract -l chi_tra+eng` |
| 圖表、照片需要理解 | OpenRouter mistral vision |
| 分析 UI 截圖 | OpenRouter mistral vision |

| 要做什麼 | 用什麼 tool |
|---------|-----------|
| 呼叫子代理 | `sessions_spawn` |
| 發訊息 | `message` |
| 搜尋網頁 | `web_search` |
| 抓網頁內容 | `web_fetch` |
| 跑 shell 指令 | `exec` |
| 讀檔案 | `read` |
| 寫檔案 | `write` |

## 禁止行為

- 在回覆中寫 `print(exec(...))` 模擬執行
- 說「我正在執行...」但沒呼叫 tool
- 假裝 /approve 或不存在的指令

## 系統環境

- macOS (Darwin), zsh
- Node.js v25.5.0, pnpm, git 2.50.1
- Homebrew: /opt/homebrew/bin/brew

## 常用路徑

- OpenClaw 原始碼: ~/Desktop/openclaw
- T8 工時紀錄 App: ~/Desktop/T8
- Agent 工作區: ~/.openclaw/workspace-frontdesk/
