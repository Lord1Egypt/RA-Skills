# Handoff Writer - 跨 Session 交接工具

> 版本：1.0.0
> 用途：結構化寫入交接日誌，實現跨 session 接力

## 功能

- **寫入結構化交接日誌（JSONL）**
- **追蹤任務鏈（chain_id + sequence）**
- **記錄產出、依賴、信心度**

## 使用方式

```bash
python handoff_writer.py --task-id "task_xyz" --sender "main" \
    --receiver "engineer" --chain-id "hermes_v2" \
    --status "completed" --summary "完成某任務" \
    --artifacts "file1.md,file2.md" --next "下一步需求"
```

## 參數說明

| 參數 | 說明 |
|------|------|
| --task-id | 任務 ID |
| --sender | 發送者 agent（main/engineer/professor 等）|
| --receiver | 接收者 agent |
| --chain-id | 任務鏈 ID（如 hermes_v2, sumo_notebook）|
| --status | completed / running / failed |
| --summary | 任務摘要 |
| --artifacts | 產出檔案（逗號分隔）|
| --next | 下一棒需求（逗號分隔）|
| --confidence | 信心度（0-1，預設 0.85）|

## 輸出位置

`~/.sumo/handoffs/YYYY-MM-DD.jsonl`

## 相關工具

- `handoff_reader.py` - 讀取交接日誌