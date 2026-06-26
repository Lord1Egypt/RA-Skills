---
name: mirofish-predict
description: "MiroFish 群體智能推演引擎。當用戶要求「推演」「預測」「模擬」「如果…會怎樣」時使用。透過 55 個 AI Agent 在模擬社交平台上互動推演未來趨勢。"
homepage: https://github.com/666ghj/MiroFish
metadata:
  {
    "openclaw":
      {
        "emoji": "🐟",
        "requires": { "bins": ["mirofish", "docker"], "env": ["LLM_API_KEY"] },
        "primaryEnv": "LLM_API_KEY",
        "install":
          [
            {
              "id": "mirofish-npm",
              "kind": "node",
              "package": "mirofish-cli",
              "bins": ["mirofish"],
              "label": "Install MiroFish CLI (npm)",
            },
          ],
      },
  }
---

# MiroFish 群體智能推演

用 55 個 AI Agent 在模擬的 Twitter/Reddit 上互動，推演未來趨勢。

## 一鍵推演

```bash
mirofish predict "如果比特幣突破15萬美元，加密市場會怎樣？"
```

自動完成：啟動 Docker 後端 → 建立專案 → 構建知識圖譜 → 生成 Agent → 運行模擬 → 輸出報告。

## 首次設定

需要 Docker Desktop 和 LLM API key。

```bash
# 1. 啟動（首次會自動拉 Docker image）
mirofish serve start
# → 如果沒有 ~/.mirofish/.env，會生成模板讓你填 API key

# 2. 配置 API key 後重新啟動
mirofish serve start
```

### API Key 設定方式

- 環境變數：`export LLM_API_KEY=xxx`
- OpenClaw config：`skills."mirofish-predict".env.LLM_API_KEY`
- 檔案：`~/.mirofish/.env`

## 命令參考

| 命令 | 功能 |
|:---|:---|
| `mirofish predict "主題"` | 完整推演（自動啟動後端） |
| `mirofish predict "主題" --rounds=10` | 指定推演輪數 |
| `mirofish serve start` | 啟動 Docker 後端 |
| `mirofish serve stop` | 停止後端 |
| `mirofish serve status` | 檢查後端狀態 |
| `mirofish projects` | 列出所有專案 |
| `mirofish status <sim_id>` | 查詢模擬進度 |
| `mirofish report <sim_id>` | 取得推演報告 |
| `mirofish chat <sim_id> "問題"` | 對報告追問 |
| `mirofish interview <sim_id> <agent_id> "問題"` | 採訪特定 Agent |
| `mirofish env` | 顯示設定狀態 |

## 追問

```bash
mirofish chat <sim_id> "哪些 KOL 的觀點最極端？"
mirofish interview <sim_id> 0 "你對 BTC 破 15 萬有什麼看法？"
```

## 注意事項

- 推演消耗大量 LLM token（55 Agent × N 輪），本地模型可節省費用
- `--rounds` 建議 10-20 輪先試，效果好再加到 40
- `--platform` 可選 `twitter`、`reddit`、`parallel`（推薦 parallel）
- 建議 LLM ≥ 14B 參數
