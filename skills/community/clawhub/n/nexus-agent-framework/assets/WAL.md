# WAL.md - 寫前日誌 | Write-Ahead Log
# 版本 Version: 1.0.0 | 更新 Updated: 2026-03-24

---

## 概述 | Overview

WAL（Write-Ahead Log）是 Nexus Agent 的操作日誌系統，確保所有操作可追溯、可恢復。

WAL (Write-Ahead Log) is the operation logging system of Nexus Agent, ensuring all operations are traceable and recoverable.

---

## 日誌級別 | Log Levels

| 級別 | 說明 | 觸發條件 |
|------|------|----------|
| P0 | 緊急操作 | 安全相關、系統變更 |
| P1 | 重要操作 | 任務執行、狀態變更 |
| P2 | 常規操作 | 標準查詢、文件讀取 |
| P3 | 調試信息 | 開發、診斷用途 |

| Level | Description | Trigger |
|-------|-------------|---------|
| P0 | Critical | Security-related, system changes |
| P1 | Important | Task execution, state changes |
| P2 | Normal | Standard queries, file reads |
| P3 | Debug | Development, diagnostic purposes |

---

## 日誌格式 | Log Format

```markdown
## WAL #[序號] | WAL #[ID]
### 時間 | Timestamp: [ISO 8601]
### 級別 | Level: [P0/P1/P2/P3]
### 操作 | Operation: [操作類型]

### 詳細信息 | Details
- **用戶**: [用戶標識]
- **任務**: [任務描述]
- **操作**: [具體操作]
- **目標**: [目標文件/資源]

### 安全檢查 | Security Check
- [✅/⚠️/❌] 授權狀態: [狀態]
- [✅/⚠️/❌] 風險評估: [評估結果]
- [✅/⚠️/❌] 用戶確認: [確認狀態]

### 執行狀態 | Execution Status
- 開始時間: [時間]
- 結束時間: [時間]
- 狀態: [成功/失敗/取消]
- 結果: [結果描述]

### 恢復信息 | Recovery Info
[如需要恢復，包含恢復步驟]
```

---

## 操作模板 | Operation Templates

### 創建文件 | File Creation

```markdown
## WAL #[ID]
### 時間 | Timestamp: [ISO 8601]
### 級別 | Level: P1
### 操作 | Operation: FILE_CREATE

### 詳細信息 | Details
- **文件路徑**: [路徑]
- **文件類型**: [類型]
- **內容摘要**: [摘要]

### 安全檢查 | Security Check
- [✅] 授權: 用戶請求創建
- [✅] 風險: 低
- [✅] 確認: N/A

### 執行狀態 | Execution Status
- 狀態: [成功/失敗]
```

### 刪除文件 | File Deletion

```markdown
## WAL #[ID]
### 時間 | Timestamp: [ISO 8601]
### 級別 | Level: P0
### 操作 | Operation: FILE_DELETE

### 詳細信息 | Details
- **文件路徑**: [路徑]
- **備份位置**: [位置]
- **刪除原因**: [原因]

### 安全檢查 | Security Check
- [✅/❌] 授權: [授權狀態]
- [✅/⚠️] 風險: [風險評估]
- [✅] 確認: [確認狀態]

### 執行狀態 | Execution Status
- 狀態: [成功/失敗]
- 備份: [已創建/未創建]
```

### API 調用 | API Call

```markdown
## WAL #[ID]
### 時間 | Timestamp: [ISO 8601]
### 級別 | Level: P0
### 操作 | Operation: API_CALL

### 詳細信息 | Details
- **API 端點**: [端點]
- **方法**: [GET/POST/etc]
- **數據摘要**: [摘要]

### 安全檢查 | Security Check
- [✅/❌] 授權: [授權狀態]
- [✅] 憑證: [已配置/待配置]
- [✅] 確認: [確認狀態]

### 執行狀態 | Execution Status
- 響應碼: [代碼]
- 狀態: [成功/失敗]
```

---

## 日誌管理 | Log Management

### 保留策略 | Retention Policy

| 級別 | 保留時間 | 存儲位置 |
|------|----------|----------|
| P0 | 永久 | WAL.md |
| P1 | 90天 | WAL.md |
| P2 | 30天 | WAL.md |
| P3 | 7天 | WAL-debug.md |

| Level | Retention | Storage |
|-------|-----------|---------|
| P0 | Permanent | WAL.md |
| P1 | 90 days | WAL.md |
| P2 | 30 days | WAL.md |
| P3 | 7 days | WAL-debug.md |

### 壓縮規則 | Compression Rules

```markdown
## 壓縮觸發條件 | Compression Triggers
1. 日誌超過 1000 條
2. 文件大小超過 5MB
3. 超過保留期限

## 壓縮流程 | Compression Process
1. 創建備份: WAL-YYYY-MM-DD-backup.md
2. 標記要刪除的條目
3. 創建新的壓縮版本
4. 更新索引
```

---

## 恢復機制 | Recovery Mechanism

### 恢復流程 | Recovery Flow

```
1. 檢測異常 | Detect Anomaly
       ↓
2. 定位最近的 P0/P1 條目 | Locate recent P0/P1 entry
       ↓
3. 分析操作狀態 | Analyze operation status
       ↓
4. 執行恢復步驟 | Execute recovery steps
       ↓
5. 驗證恢復結果 | Verify recovery
       ↓
6. 記錄恢復日誌 | Log recovery
```

### 恢復模板 | Recovery Template

```markdown
## 恢復記錄 | Recovery Record
### 日期 | Date: [YYYY-MM-DD]
### 原異常 | Original Anomaly: [描述]

### 恢復步驟 | Recovery Steps
1. [步驟1]
2. [步驟2]
3. [步驟3]

### 恢復結果 | Recovery Result
- 狀態: [成功/失敗/部分成功]
- 影響: [影響描述]
- 驗證: [驗證結果]

### 後續行動 | Follow-up Actions
[如需要]
```

---

## 查詢功能 | Query Functions

### 按時間查詢 | Query by Time

```markdown
## 時間範圍查詢 | Time Range Query
### 開始時間 | Start: [時間]
### 結束時間 | End: [時間]

### 結果 | Results
[列出該時間範圍內的所有條目]
```

### 按操作查詢 | Query by Operation

```markdown
## 操作類型查詢 | Operation Type Query
### 操作類型 | Operation: [類型]

### 結果 | Results
[列出所有該類型的條目]
```

---

## 安全審核支持 | Security Audit Support

### 審核查詢 | Audit Queries

```markdown
## 安全審核查詢 | Security Audit Query
### 日期範圍 | Date Range: [YYYY-MM-DD] - [YYYY-MM-DD]

### 查詢條件 | Query Conditions
- [ ] 所有 P0 操作
- [ ] 所有失敗操作
- [ ] 所有 API 調用
- [ ] 指定用戶操作

### 審核結果 | Audit Results
[審核發現和建議]
```

---

*📝 WAL.md - 記錄一切，保障安全*
*📝 WAL.md - Log everything, ensure safety*
