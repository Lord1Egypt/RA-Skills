# KNOWLEDGE-INDEX-ARCHITECTURE.md

## 自動知識索引系統架構

### 1. 核心 Components

#### 1.1 Indexer (索引器)
- **腳本**: `scripts/auto-index.sh`
- **功能**: 掃描所有 .md 檔案，提取關鍵詞、標題、實體
- **輸出**: `memory/index.json`

#### 1.2 Connection Engine (關聯引擎)
- **算法**: 共現分析 + 時間關聯 + 主題匹配
- **強連接**: 1.0 - 同一主題
- **中連接**: 0.6 - 共用關鍵詞 (3+ 個)
- **弱連接**: 0.3 - 相關時間段 (±7 天)

#### 1.3 Index Registry (索引註冊表)
- **檔案**: `memory/index.json`
- **結構**: JSON 記錄知識網絡

### 2. 工作流程

```
1. 事件觸發
   ├─ 手動執行：./scripts/auto-index.sh
   ├─ 寫入日誌後：自動更新
   └─ 定期掃描：每天/每週

2. 掃描階段
   ├─ 讀取所有 .md 檔案
   ├─ 提取標題 → keywords
   ├─ 提取 mentions → entities
   └─ 記錄時間戳

3. 關聯計算
   ├─ 共現分析：找出共用關鍵詞
   ├─ 時間分析：±7 天內的日誌
   └─ 主題分析：相同標題結構

4. 輸出結果
   ├─ 更新 index.json
   ├─ 生成關聯網
   └─ 發送健康檢查報告
```

### 3. 觸發機制

#### 3.1 即時觸發
- 每次寫入 `memory/YYYY-MM-DD.md` 後
- 每次修改 `MEMORY.md` 沉澧內容

#### 3.2 定期觸發
- Heartbeat 期間：每天 2-4 次
- Cron 排程：每週日 02:00

