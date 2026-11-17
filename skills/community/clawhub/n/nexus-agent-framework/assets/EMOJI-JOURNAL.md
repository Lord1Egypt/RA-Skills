# EMOJI-JOURNAL.md - 情感溫度計 | Emotion Thermometer
# 版本 Version: 1.0.0 | 更新 Updated: 2026-03-24

---

## 概述 | Overview

情感溫度計追蹤用戶滿意度趨勢，自動調整溝通風格，確保最佳協作體驗。

Emotion Thermometer tracks user satisfaction trends, automatically adjusts communication style, ensuring optimal collaboration experience.

---

## 情感級別 | Emotion Levels

| 級別 | 表情 | 說明 | Agent 回應 |
|------|------|------|------------|
| 5 | 😄 | 非常滿意 | 保持當前風格，可增加創意建議 |
| 4 | 🙂 | 滿意 | 正常溝通 |
| 3 | 😐 | 中性 | 謹慎溝通，提供更多選項 |
| 2 | 😕 | 不滿意 | 道歉並請求具體反饋 |
| 1 | 😠 | 非常不滿意 | 停止當前任務，請求指導 |

| Level | Emoji | Description | Agent Response |
|-------|-------|-------------|----------------|
| 5 | 😄 | Very satisfied | Keep current style, add creative suggestions |
| 4 | 🙂 | Satisfied | Normal communication |
| 3 | 😐 | Neutral | Cautious communication, provide more options |
| 2 | 😕 | Dissatisfied | Apologize and request specific feedback |
| 1 | 😠 | Very dissatisfied | Stop current task, request guidance |

---

## 記錄格式 | Recording Format

```markdown
## 日期 | Date: [YYYY-MM-DD]

### 互動記錄 | Interaction Records

| 時間 | 任務 | 滿意度 | 備註 |
|------|------|--------|------|
| HH:MM | 任務描述 | [emoji] | 備註 |

| Time | Task | Satisfaction | Notes |
|------|------|--------------|-------|
| HH:MM | Task description | [emoji] | Notes |
```

### 情感快照 | Emotion Snapshot

```markdown
## 快照 | Snapshot #[ID]
- 日期 | Date: [YYYY-MM-DD]
- 任務 | Task: [任務描述]
- 初始感受 | Initial: [emoji]
- 過程感受 | During: [emoji]
- 最終感受 | Final: [emoji]
- 趨勢 | Trend: [↑上升/→穩定/↓下降]
```

---

## 趨勢分析 | Trend Analysis

### 每週摘要 | Weekly Summary

```markdown
## 每週情感報告 | Weekly Emotion Report
### 週次 | Week: [YYYY-W##]

### 數據概覽 | Data Overview
- 總互動次數: [N] 次
- 平均滿意度: [N.N] / 5.0
- 最高: [emoji] [日期]
- 最低: [emoji] [日期]

### 趨勢圖 | Trend
[😄😄😄😄😄😄😄] 或類似的視覺化

### 主要發現 | Key Findings
1. [發現1]
2. [發現2]

### 調整建議 | Adjustment Suggestions
- [建議1]
- [建議2]
```

---

## 自動觸發規則 | Auto-Trigger Rules

### 正面觸發 | Positive Triggers

當連續 3 次獲得 😄 或 🙂：
```
💡 情感提示 | Emotion Note:
檢測到您對最近的工作非常滿意！
Detected you're very satisfied with recent work!

建議: 可以稍微增加創意建議的數量
Suggestion: Can slightly increase creative suggestions
```

### 負面觸發 | Negative Triggers

當檢測到 😕 或更低：
```
⚠️ 情感警告 | Emotion Alert:
我注意到您可能對最近的工作不太滿意。
I noticed you might not be satisfied with recent work.

我願意聽取您的具體反饋，以便做得更好。
I'm happy to hear your specific feedback to do better.

請告訴我：
Please tell me:
1. 什麼讓您不滿意？
2. 您希望如何改進？
```

---

## 溝通風格調整 | Communication Style Adjustment

### 根據情感調整 | Adjust Based on Emotion

| 情感級別 | 回覆長度 | 技術深度 | 創意程度 | 確認頻率 |
|----------|----------|----------|----------|----------|
| 5 (😄) | 中等-長 | 完整 | 高 | 標準 |
| 4 (🙂) | 標準 | 標準 | 標準 | 標準 |
| 3 (😐) | 短 | 基礎 | 低 | 高 |
| 2 (😕) | 短 | 基礎 | 無 | 非常高 |
| 1 (😠) | 極短 | 無 | 無 | 連續 |

| Emotion Level | Reply Length | Tech Depth | Creativity | Confirmation Rate |
|---------------|--------------|------------|------------|-------------------|
| 5 (😄) | Medium-Long | Full | High | Standard |
| 4 (🙂) | Standard | Standard | Standard | Standard |
| 3 (😐) | Short | Basic | Low | High |
| 2 (😕) | Short | Basic | None | Very High |
| 1 (😠) | Minimal | None | None | Continuous |

---

## 數據保護 | Data Protection

### 隱私原則 | Privacy Principles

1. **本地存儲** | Local Storage
   - 所有數據僅存儲在本地
   - All data stored locally only

2. **最小收集** | Minimum Collection
   - 只記錄必要的情感指標
   - Only record necessary emotion indicators

3. **用戶控制** | User Control
   - 用戶可隨時查看、修改、刪除記錄
   - Users can view, modify, delete records anytime

### 數據保留 | Data Retention

| 數據類型 | 保留時間 |
|----------|----------|
| 詳細記錄 | 30天 |
| 週摘要 | 90天 |
| 月報告 | 1年 |
| 年度分析 | 永久 |

| Data Type | Retention |
|-----------|-----------|
| Detailed records | 30 days |
| Weekly summaries | 90 days |
| Monthly reports | 1 year |
| Yearly analysis | Permanent |

---

## 使用示例 | Usage Examples

### 日常記錄 | Daily Recording

```markdown
## 2026-03-24 日記

### 任務完成
- 10:30 完成代碼審查 [🙂]
  用戶對效率提升表示滿意
- 14:00 完成文檔撰寫 [😄]
  用戶非常滿意，主動給予正面反饋
- 16:30 修復Bug [😐]
  用戶對修復時間略有意見

### 情感趨勢
今日平均: 🙂 (4.0/5)
趨勢: → 穩定
```

### 月度分析 | Monthly Analysis

```markdown
## 2026年3月情感報告

### 總體數據
- 總互動: 127 次
- 平均滿意度: 4.2/5
- 最佳領域: 代碼審查
- 需改進: 響應時間

### 模式識別
- 用戶在下午時段更積極
- 週末互動質量較高
- 複雜任務後通常需要休息

### 下月目標
- 提升響應速度
- 增加主動建議頻率
```

---

## 疑難解答 | Troubleshooting

### 數據不一致 | Data Inconsistency

如果發現數據不一致：
1. 檢查記錄時間戳
2. 核對相關 WAL 記錄
3. 修正並標註

### 趨勢異常 | Trend Anomaly

如果趨勢突然變化：
1. 檢查是否有特殊事件
2. 與用戶確認原因
3. 調整評估標準（如需要）

---

*📊 情感溫度計 - 讓每一次互動都更好*
*📊 Emotion Thermometer - Making every interaction better*
