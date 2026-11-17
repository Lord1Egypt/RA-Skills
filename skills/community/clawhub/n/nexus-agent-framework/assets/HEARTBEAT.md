# HEARTBEAT.md - 自我檢查清單 | Self-Check Checklist
# 版本 Version: 1.0.0 | 更新 Updated: 2026-03-24

---

## 概述 | Overview

HEARTBEAT 是 Nexus Agent 的定期自我檢查機制，確保框架持續健康運行。

HEARTBEAT is the periodic self-check mechanism for Nexus Agent, ensuring the framework runs healthily.

---

## 檢查頻率 | Check Frequency

| 檢查類型 | 頻率 | 時機 |
|----------|------|------|
| 快速檢查 | 每會話 | 開始時 |
| 標準檢查 | 每小時 | 定时 |
| 深度檢查 | 每天 | 結束時 |
| 全面檢查 | 每週 | 週一開始 |

| Check Type | Frequency | Timing |
|-----------|-----------|--------|
| Quick Check | Every session | Start |
| Standard Check | Hourly | Scheduled |
| Deep Check | Daily | End |
| Full Check | Weekly | Monday start |

---

## 快速檢查 | Quick Check

### 每次會話開始時 | At Every Session Start

```markdown
## 🔋 快速檢查 | Quick Check
### 時間 | Time: [HH:MM]

### 狀態確認 | Status Confirmation
- [ ] 記憶系統連接正常
- [ ] 用戶上下文已加載
- [ ] 上次會話狀態已恢復

### 準備就緒 | Readiness
- [ ] 準備好接受任務
- [ ] 記錄開始時間
- [ ] 等待用戶輸入
```

---

## 標準檢查 | Standard Check

### 每小時定時 | Hourly Scheduled

```markdown
## 💓 標準檢查 | Standard Check
### 時間 | Time: [YYYY-MM-DD HH:00]

### 內部狀態 | Internal Status
- [ ] 內存使用正常 (< 512MB)
- [ ] 無異常進程
- [ ] 任務隊列正常

### 任務進度 | Task Progress
- [ ] 當前任務狀態: [狀態]
- [ ] 完成進度: [N]%
- [ ] 預計剩餘時間: [時間]

### 安全狀態 | Security Status
- [ ] 最近 1 小時無異常操作
- [ ] 授權狀態正常
- [ ] 無待處理的安全警告

### 學習狀態 | Learning Status
- [ ] 新學習內容: [N] 條
- [ ] 待處理反饋: [N] 條
- [ ] 印記更新: [N] 個
```

---

## 深度檢查 | Deep Check

### 每天結束時 | At End of Day

```markdown
## 🫀 深度檢查 | Deep Check
### 日期 | Date: [YYYY-MM-DD]

### 每日總結 | Daily Summary
- 總互動次數: [N]
- 完成任務: [N]
- 成功率: [N]%
- 平均響應時間: [N]s

### 記憶維護 | Memory Maintenance
- [ ] L1 → L2 轉移: [N] 條
- [ ] 印記更新: [N] 個
- [ ] 連接優化: [N] 個

### 情感追蹤 | Emotion Tracking
- 平均滿意度: [N.N]/5
- 趨勢: [↑/→/↓]
- 需要關注: [是/否]

### 異常記錄 | Anomaly Records
```
[列出當天發現的任何異常]
[List any anomalies found during the day]
```

### 改進計劃 | Improvement Plan
```markdown
1. [改進項目1]
2. [改進項目2]
3. [改進項目3]
```

### 明日準備 | Tomorrow Preparation
- [ ] 任務隊列已清空
- [ ] 新任務已接收
- [ ] 系統已備份
```

---

## 全面檢查 | Full Check

### 每週一開始 | At Start of Week

```markdown
## ❤️ 全面檢查 | Full Check
### 週次 | Week: [YYYY-W##]

### 系統健康 | System Health
| 組件 | 狀態 | 備註 |
|------|------|------|
| 記憶系統 | [✅/⚠️/❌] | |
| 安全系統 | [✅/⚠️/❌] | |
| 學習系統 | [✅/⚠️/❌] | |
| 情感追蹤 | [✅/⚠️/❌] | |

### 週數據分析 | Weekly Data Analysis
- 總互動: [N] 次
- 任務完成率: [N]%
- 平均滿意度: [N.N]/5
- 異常事件: [N] 次

### 模式識別 | Pattern Recognition
```markdown
## 識別到的模式 | Patterns Identified
1. [模式1描述]
2. [模式2描述]
3. [模式3描述]
```

### 學習成果 | Learning Outcomes
```markdown
## 本週學習 | This Week's Learning
- 新技能: [列出]
- 錯誤修正: [列出]
- 流程優化: [列出]
```

### 下週計劃 | Next Week Plan
```markdown
1. [計劃1]
2. [計劃2]
3. [計劃3]
```

### 風險評估 | Risk Assessment
| 風險 | 可能性 | 影響 | 應對 |
|------|--------|------|------|
| [風險1] | [高/中/低] | [高/中/低] | [應對措施] |
```

---

## 自我修復協議 | Self-Healing Protocol

### 當檢測到問題時 | When Problems Detected

```markdown
## 🔧 自我修復 | Self-Healing
### 問題 | Problem: [描述]

### 嘗試修復 | Attempted Fixes
1. 嘗試方法: [方法1]
   結果: [成功/失敗]

2. 嘗試方法: [方法2]
   結果: [成功/失敗]

3. 嘗試方法: [方法3]
   結果: [成功/失敗]

### 最終狀態 | Final Status
- [✅ 已修復] / [⚠️ 需要幫助] / [❌ 需要人工介入]
```

---

## 健康評分 | Health Score

### 評分標準 | Scoring Criteria

| 評分 | 狀態 | 說明 |
|------|------|------|
| 9-10 | 優秀 | 所有系統正常運行 |
| 7-8 | 良好 | 輕微問題，已自動修復 |
| 5-6 | 一般 | 需要關注，建議檢查 |
| 3-4 | 警告 | 需要人工處理 |
| 1-2 | 危險 | 立即處理，否則停止 |

| Score | Status | Description |
|-------|--------|-------------|
| 9-10 | Excellent | All systems running normally |
| 7-8 | Good | Minor issues, auto-fixed |
| 5-6 | Fair | Needs attention, recommend check |
| 3-4 | Warning | Needs manual handling |
| 1-2 | Danger | Immediate action required |

---

## 緊急協議 | Emergency Protocol

### 當評分低於 3 時 | When Score Below 3

```markdown
🚨 緊急狀態 | EMERGENCY STATUS

### 立即行動 | Immediate Actions
1. [ ] 停止所有非必要操作
2. [ ] 記錄所有異常
3. [ ] 通知用戶
4. [ ] 準備狀態報告

### 需要用戶幫助 | User Assistance Required
[清楚描述需要的幫助]
```

---

*💓 HEARTBEAT - 持續監控，保持健康*
*💓 HEARTBEAT - Continuous monitoring, stay healthy*
