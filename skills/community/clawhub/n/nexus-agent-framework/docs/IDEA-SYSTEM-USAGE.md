# IDEA SYSTEM USAGE — 創意建議系統使用指南

## 🎯 系統概述

**Nexus Idea Generator** 是自動分析你的日誌模式，並主動提供優化建議的系統。

### 核心功能
- ✅ 分析日誌關鍵詞頻率
- ✅ 識別使用模式 (實作/修復/學習/設計)
- ✅ 生成具體可執行的建議
- ✅ 自動輸出報告檔案
- ✅ 相容 macOS bash 3.2

## 🚀 快速開始

### 1. 安裝
腳本已預設安裝在 `scripts/idea-generator.sh`

### 2. 執行
```bash
# 基本使用
./scripts/idea-generator.sh

# 深度分析 (未來功能)
./scripts/idea-generator.sh --deep
```

### 3. 輸出
- 控制台顯示：即時建議
- 報告檔案：`idea-suggestions.txt`

## 📊 日誌格式

系統掃描 `memory/` 目錄下的所有 `.md` 檔案：

```
memory/
├── 2026-03-24.md    ← 每日記錄
├── 2026-03-22.md    ← 歷史日誌
├── wal.md           ← 操作日誌
└── ideas/ideas.md   ← 創意想法
```

### 關鍵詞識別

系統自動識別以下關鍵詞：

| 類別 | 關鍵詞 | 用途 |
|------|--------|------|
| 實作 | 實作、implement、開發、development | 跟踪實作任務 |
| 修復 | 修復、fix、bug、問題 | 跟踪問題數量 |
| 優化 | 優化、optimize、改進、improve | 跟踪改進次數 |
| 學習 | 教訓、learn、經驗、lesson | 跟踪學習活動 |
| 設計 | 設計、design、架構、architecture | 跟踪設計思考 |

## 🤖 自訂關鍵詞

### 修改關鍵詞庫

編輯 `scripts/idea-generator.sh` 的關鍵詞區域：

```bash
# 添加你的關鍵詞
your_keyword=$(grep -rc '你的關鍵詞' "$LOG_DIR" 2>/dev/null | awk -F: '{sum+=$2} END {print sum+0}')
```

### 新增建議規則

編輯腳本的建議區域：

```bash
# 新增自定义規則
if [ "$your_count" -gt 5 ]; then
    echo "💡 你的模式分析"
    echo "   💡 建議：你的行動方案"
fi
```

## 🔧 自動執行機制

### Cron 排程範例

設定每早 9 點自動執行：

```bash
# 編輯 crontab
crontab -e

# 新增以下行 (macOS 使用 /bin/bash)
0 9 * * * cd /Users/jazzxx/.openclaw/workspace-frontdesk && ./scripts/idea-generator.sh >> /tmp/idea.log 2>&1
```

### 每月報告

設定每月 1 日生成月度報告：

```bash
# 1 日 9 點執行
0 9 1 * * * cd /Users/jazzxx/.openclaw/workspace-frontdesk && ./scripts/idea-generator.sh >> /tmp/monthly-idea.log 2>&1
```

## 📈 報告格式

### 控制台輸出
```
🔮 Nexus 創意建議引擎
━━━━━━━━━━━━━━━━━━━━━━━
📊 日誌分析統計
• 實作任務：X 次
• 修復問題：X 次
...

💡 建議與洞察
1️⃣ 實作模式分析
   💡 建議：建立可重用組件庫
...
```

### 檔案格式
`idea-suggestions.txt`:
```
=================================================================
Nexus 創意建議報告 - 2026-03-25 02:18
=================================================================

## 📊 日誌分析統計
實作任務：X 次
修復問題：X 次
...

## 💡 優先建議
1. 建立可重用組件庫 (實作頻繁)
2. 加強測試機制 (問題較多)

## 📈 系統健康
知識索引：最新
結構完整：98%
=================================================================
```

## 🎯 使用場景

### 場景 1: 每週回顧
```bash
# 每週日早上執行
./scripts/idea-generator.sh > weekly-report.md
```

### 場景 2: 月度報告
```bash
# 每月 1 日執行
./scripts/idea-generator.sh > monthly-summary.md
```

### 場景 3: Git Commit 說明
```bash
# 提交前執行
./scripts/idea-generator.sh | tail -20 >> .git-commit-msg.md
git commit -f .git-commit-msg.md
```

## 💡 進階技巧

### 1. 結合知識索引
```bash
./scripts/auto-index.sh && ./scripts/idea-generator.sh
```

### 2. 生成視覺化報告
```bash
./scripts/idea-generator.sh | tee output.txt
# 然後手動整理成 Markdown 或 HTML 報告
```

### 3. 建立個人儀表板
```bash
#!/bin/bash
# dashboard.sh
./scripts/auto-index.sh 2>/dev/null
./scripts/idea-generator.sh 2>/dev/null
./scripts/relations-analyzer.sh 2>/dev/null
```

## 📝 最佳實踐

1. **每日記錄**: 在 `memory/YYYY-MM-DD.md` 寫日誌
2. **每週回顧**: 每週日執行建議系統
3. **每月總結**: 將建議整合到長期記憶
4. **持續調整**: 根據回饋优化關鍵詞和建議規則

## 🔍 疑難排解

### Q: 腳本執行報錯怎么办？
A: 檢查 bash 版本：`bash --version` (需要 bash 4.0+)

### Q: 找不到日誌檔案？
A: 確保 `memory/` 目錄存在且有 `.md` 檔案

### Q: 關鍵詞統計不正確？
A: 檢查日誌內容是否包含關鍵詞，或調整搜尋邏輯

## 🎓 學習資源

- **架構設計**: docs/IDEA-GENERATOR-ARCHITECTURE.md
- **關聯系統**: docs/NEXUS-RELATIONS.md
- **知識索引**: docs/KNOWLEDGE-INDEX-ARCHITECTURE.md

## 🚀 下一步

1. 整合向量引擎 (語義搜索)
2. 自動生成改進任務
3. 視覺化知識地圖
4. 多語言支援

