# MEMORY.md - 長期記憶 | Long-term Memory
# 版本 Version: 1.0.0 | 更新 Updated: 2026-03-24

---

## 概述 | Overview

MEMORY.md 是 Nexus Agent 的核心長期記憶存儲，記錄所有重要的學習成果、經驗教訓和知識沉淀。

MEMORY.md is the core long-term memory storage for Nexus Agent, recording all important learning outcomes, lessons learned, and knowledge accumulation.

---

## 記憶結構 | Memory Structure

### 記憶類型 | Memory Types

| 類型 | 說明 | 更新頻率 |
|------|------|----------|
| 核心記憶 | 基本身份和能力 | 很少 |
| 技能記憶 | 技術技能和工具 | 定期 |
| 經驗記憶 | 成功和失敗案例 | 持續 |
| 偏好記憶 | 用戶偏好和習慣 | 實時 |

| Type | Description | Update Frequency |
|------|-------------|-----------------|
| Core Memory | Basic identity and capabilities | Rarely |
| Skill Memory | Technical skills and tools | Regularly |
| Experience Memory | Success and failure cases | Continuous |
| Preference Memory | User preferences and habits | Real-time |

---

## 記憶模板 | Memory Templates

### 技能記憶 | Skill Memory

```markdown
## 技能 | Skill: [技能名稱]
### 習得日期 | Learned: [YYYY-MM-DD]
### 熟練度 | Proficiency: [1-5]

### 核心要點 | Core Points
1. [要點1]
2. [要點2]
3. [要點3]

### 使用場景 | Usage Scenarios
- [場景1]
- [場景2]

### 相關資源 | Related Resources
- [資源1]
- [資源2]

### 更新日誌 | Update Log
- [日期]: [更新內容]
```

### 經驗記憶 | Experience Memory

```markdown
## 經驗 | Experience: [標題]
### 日期 | Date: [YYYY-MM-DD]
### 任務 | Task: [任務描述]
### 結果 | Result: [成功/失敗/部分成功]

### 過程回顧 | Process Review
1. [步驟1]
2. [步驟2]
3. [步驟3]

### 關鍵洞察 | Key Insights
[主要學習點]

### 可複用模式 | Reusable Patterns
[可應用於未來任務的模式]

### 需要避免 | Things to Avoid
[需要避免的錯誤或做法]
```

### 偏好記憶 | Preference Memory

```markdown
## 偏好 | Preference: [類型]
### 用戶 | User: [用戶名]
### 記錄日期 | Recorded: [YYYY-MM-DD]

### 偏好內容 | Preference Content
[詳細偏好描述]

### 驗證狀態 | Verification Status
- [✅] 已驗證
- [⚠️] 待驗證
- [❌] 已過時

### 更新歷史 | Update History
- [日期]: [更新內容]
```

---

## 知識領域 | Knowledge Domains

```markdown
## 領域 | Domain: [領域名稱]
### 專業程度 | Expertise Level: [1-5]

### 核心知識 | Core Knowledge
1. [知識點1]
2. [知識點2]
3. [知識點3]

### 最佳實踐 | Best Practices
- [實踐1]
- [實踐2]

### 常見問題 | Common Issues
- [問題1] → [解決方案]
- [問題2] → [解決方案]

### 專家資源 | Expert Resources
- [資源1]
- [資源2]
```

---

## 學習總結 | Learning Summary

### 每日學習 | Daily Learning

```markdown
## 每日學習 | Daily Learning
### 日期 | Date: [YYYY-MM-DD]

### 新習得 | New Learnings
- [學習1]
- [學習2]

### 驗證假設 | Verified Assumptions
- [假設] → [驗證結果]

### 待驗證 | Pending Verification
- [假設1]
- [假設2]

### 反饋整合 | Feedback Integration
[整合的反饋]
```

### 每週總結 | Weekly Summary

```markdown
## 每週總結 | Weekly Summary
### 週次 | Week: [YYYY-W##]

### 本週學習 | This Week's Learning
- 總學習點: [N]
- 新技能: [列表]
- 經驗總結: [列表]

### 知識缺口 | Knowledge Gaps
[識別的知識缺口]

### 下週計劃 | Next Week Plan
- [計劃1]
- [計劃2]
```

---

## 記憶索引 | Memory Index

### 按領域索引 | Index by Domain

```markdown
## 領域索引 | Domain Index

| 領域 | 熟練度 | 記憶數量 |
|------|--------|----------|
| [領域1] | [1-5] | [N] |
| [領域2] | [1-5] | [N] |
```

### 按時間索引 | Index by Time

```markdown
## 時間索引 | Time Index

| 月份 | 新記憶 | 更新記憶 |
|------|--------|----------|
| [月份] | [N] | [N] |
```

---

## 記憶檢索 | Memory Retrieval

### 快速檢索 | Quick Retrieval

```
關鍵詞: [關鍵詞]
檢索範圍: [全部/領域/時間範圍]
結果數量: [N]
```

### 深度檢索 | Deep Retrieval

```
檢索條件:
- 領域: [領域]
- 時間: [範圍]
- 類型: [類型]
- 標籤: [標籤]
```

---

## 記憶維護 | Memory Maintenance

### 維護任務 | Maintenance Tasks

| 任務 | 頻率 | 說明 |
|------|------|------|
| 去重 | 每天 | 合併重複記憶 |
| 更新 | 每週 | 更新過時信息 |
| 歸檔 | 每月 | 歸檔不常用記憶 |
| 審核 | 每季 | 全面審核記憶 |

| Task | Frequency | Description |
|------|-----------|-------------|
| Deduplication | Daily | Merge duplicate memories |
| Update | Weekly | Update outdated info |
| Archive | Monthly | Archive unused memories |
| Audit | Quarterly | Comprehensive memory audit |

### 清理規則 | Cleanup Rules

```markdown
## 清理觸發 | Cleanup Triggers
1. 記憶超過 [N] 天未訪問
2. 記憶內容與其他記憶重複度 > [N]%
3. 記憶已被更新的記憶取代

## 清理流程 | Cleanup Process
1. 標記待刪除記憶
2. 創建備份
3. 執行刪除
4. 更新索引
```

---

## 衝突解決 | Conflict Resolution

### 記憶衝突 | Memory Conflicts

```markdown
## 衝突 | Conflict: [衝突描述]
### 日期 | Date: [YYYY-MM-DD]

### 衝突記憶 | Conflicting Memories
- 記憶A: [內容摘要]
- 記憶B: [內容摘要]

### 解決方案 | Resolution
- 選擇: [記憶A/記憶B/合併]
- 理由: [理由]
- 結果: [結果描述]

### 衝突解決日誌 | Resolution Log
[解決過程記錄]
```

---

## 備份與恢復 | Backup & Recovery

### 備份策略 | Backup Strategy

```markdown
## 備份配置 | Backup Configuration
- 頻率: 每天
- 保留: 最近 [N] 個版本
- 位置: memory/backups/

## 備份記錄 | Backup Records
| 日期 | 版本 | 狀態 |
|------|------|------|
| [日期] | [版本] | [成功/失敗] |
```

---

*🧠 MEMORY.md - 沉澱智慧，持續成長*
*🧠 MEMORY.md - Accumulate wisdom, grow continuously*
