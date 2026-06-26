# notebooklm-rag-line

將 NotebookLM 知識自動同步到 LINE AI 助教的 RAG 知識庫。

## 特色

- 自動向 NotebookLM 提問取得答案
- 使用 bge-m3 產生 embedding 向量
- 存入本地 SQLite RAG 知識庫
- 支援 LINE 聊天機器人即時回覆
- LLM 自動生成延續問題建議

## 快速開始

### 1. 安裝依賴

```bash
pip install patchright
ollama pull bge-m3:latest
ollama pull gemma3:4b-cloud
```

### 2. 修改設定

編輯 `rag_enhance.py` 開頭的設定區塊：

```python
CHROME_PROFILE = "你的 Chrome profile 路徑"
NOTEBOOK_ID = "你的 NotebookLM 筆記本 ID"
DB_PATH = r"你的\RAG\資料庫\路徑\rag_embeddings.db"
```

### 3. 加入問題

在 `QUESTIONS` 陣列中加入問題：

```python
QUESTIONS = [
    "Cloudflare Pages 是什麼？",
    "OpenClaw 是什麼？",
]
```

### 4. 執行

```bash
python rag_enhance.py
```

## 啟動 RAG Server

```bash
python rag_server.py
```

Server 會監聽 `http://127.0.0.1:3002/query`

## 系統需求

| 元件 | 版本 |
|------|------|
| Python | 3.8+ |
| Ollama | 最新版 |
| bge-m3 | Embedding 模型 |
| gemma3:4b-cloud | LLM 模型 |

## 注意事項

- **LINE_TOKEN、RAG_URL 等金鑰請放在 `.env` 檔案，絕對不要 commit 到公開 repo**
- NotebookLM 免費版每天可問 50 次
- Embedding 可能 timeout，建議加入 warmup 設定

## 授權

MIT License