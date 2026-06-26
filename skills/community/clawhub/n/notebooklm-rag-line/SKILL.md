---
name: notebooklm-rag-line
description: 將 NotebookLM 知識自動同步到 LINE AI 助教的 RAG 知識庫，支援自動問答、向量化與延續問題建議。適用於教學助教、客服機器人或個人知識管理。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["python", "node", "ollama"] },
      "install": [
        {
          "id": "node",
          "kind": "node",
          "package": "ollama",
          "bins": ["ollama"],
          "label": "Install Ollama (Embedding + LLM)"
        }
      ]
    }
  }
---

# notebooklm-rag-line

將 NotebookLM 知識自動同步到 LINE AI 助教的 RAG 知識庫。

## 功能

- ✅ 向 NotebookLM 提問取得答案
- ✅ 自動產生 embedding（bge-m3）
- ✅ 存入本地 SQLite RAG 知識庫
- ✅ 支援 LINE 聊天機器人回覆
- ✅ LLM 生成延續問題建議

## 系統架構

```
NotebookLM 來源
    ↓（老闆新增網站）
patchright 自動提問
    ↓（取得答案）
bge-m3 embedding（Ollama）
    ↓（1024維向量）
rag_embeddings.db（SQLite）
    ↓
RAG Server (port 3002)
    ↓
line_webhook.aspx（LINE 回覆）
    ↓
學員收到回答 + 延續問題建議
```

## 核心檔案

| 檔案 | 用途 |
|------|------|
| `rag_enhance.py` | 主腳本：向 NotebookLM 提問並存入 RAG |
| `rag_server.py` | Python HTTP Server，處理學員問答 |
| `rag_embeddings.db` | SQLite 向量知識庫 |
| `line_webhook.aspx` | LINE Webhook 接收器 |

## 必要環境

| 元件 | 版本 | 備註 |
|------|------|------|
| Python | 3.8+ | 建議 3.10+ |
| Ollama | 最新版 | 安裝 `ollama serve` |
| bge-m3:latest | Embedding 模型 | `ollama pull bge-m3:latest` |
| gemma3:4b-cloud | LLM 模型 | `ollama pull gemma3:4b-cloud` |
| patchright | 最新版 | `pip install patchright` |

## 快速開始

### Step 1：安裝依賴

```bash
pip install patchright
ollama pull bge-m3:latest
ollama pull gemma3:4b-cloud
```

### Step 2：修改設定

編輯 `rag_enhance.py` 開頭的設定區塊：

```python
CHROME_PROFILE = "你的 Chrome profile 路徑"
NOTEBOOK_ID = "你的 NotebookLM 筆記本 ID"
OLLAMA_HOST = "127.0.0.1"
OLLAMA_PORT = 11434
EMBEDDING_MODEL = "bge-m3:latest"
DB_PATH = r"你的\RAG\資料庫\路徑\rag_embeddings.db"
```

### Step 3：準備問題清單

在 `QUESTIONS` 陣列中加入你想問的問題：

```python
QUESTIONS = [
    "Cloudflare Pages 是什麼？",
    "如何部署網站到 Cloudflare Pages？",
    # ... 更多問題
]
```

### Step 4：執行

```bash
python rag_enhance.py
```

腳本會自動：
1. 啟動 Chrome 並登入 NotebookLM
2. 逐一問問題（約 40 秒/題）
3. 取得答案後自動存入 RAG
4. 完成後發送 LINE 通知

## RAG Server（可選）

啟動本地 RAG Server 處理即時查詢：

```bash
python rag_server.py
```

Server 會監聽 `http://127.0.0.1:3002/query`

**Request 格式：**
```json
{
  "question": "Cloudflare Pages 是什麼？",
  "history": "[]",
  "user_id": "anonymous"
}
```

**Response 格式：**
```json
{
  "answer": "Cloudflare Pages 是...",
  "suggestions": ["問題1", "問題2", "問題3"]
}
```

## 自動化（凌晨執行）

使用 Windows Task Scheduler 每天凌晨自動更新：

```powershell
# 建立排程工作
$action = New-ScheduledTaskAction -Execute "python" -Argument "D:\node_app\cron\rag_enhance.py"
$trigger = New-ScheduledTaskTrigger -Daily -At "01:00"
Register-ScheduledTask -TaskName "RAG_NotebookLM_Update" -Action $action -Trigger $trigger -Description "NotebookLM RAG 自動更新"
```

## 資料庫結構

```sql
CREATE TABLE rag_embeddings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    embedding BLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 注意事項

- **金鑰安全**：LINE_TOKEN、RAG_URL 等敏感資訊應放在 `.env` 檔案，絕對不要 commit 到公開 repo
- **NotebookLM 配額**：免費版每天可問 50 次，注意不要超標
- **Embedding 超時**：建議加入 warmup 設定避免 timeout
- **Chrome Profile**：建議使用專用 profile，避免影響一般瀏覽器使用

## 授權

MIT License - 可自由使用、修改與發布

---

🦞 爪子鋒利，什麼都能搞定！