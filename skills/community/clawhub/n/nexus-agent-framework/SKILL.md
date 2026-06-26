---
name: nexus-agent-framework
description: 安全優先的通用 Agent 工作框架 | Secure Universal Agent Framework - 自動知識索引、創意建議、關聯系統
version: 2.0.0
metadata:
  openclaw:
    emoji: "🔮"
    homepage: https://github.com/lalawgwg99/nexus-agent-framework
    license: MIT-0
  features:
    - 🔮 自動知識索引系統
    - 💡 主動創意建議系統
    - 🔗 智能關聯分析系統
---

# 🎯 Nexus Agent Framework v2.0

**安全優先的通用 Agent 工作框架**

提供自動化知識管理、智能建議系統和關聯分析，讓您的 Agent 工作區更智能、更高效。

## ✨ 核心功能

### 🔮 自動知識索引系統

自動掃描並索引所有工作區檔案，建立知識網絡：

- **自動掃描**: 掃描所有 `.md` 檔案
- **關鍵詞提取**: 提取標題、標籤、實體
- **時標記錄**: 自動識別日期
- **JSON 索引**: 生成 `memory/index.json`

**使用:**
```bash
./scripts/auto-index.sh
```

**輸出示例:**
```json
{
  "version": "1.2",
  "files": [
    {
      "path": "memory/2026-03-24.md",
      "date": "2026-03-24",
      "keywords": ["日誌", "任務", "優化"],
      "entities": ["Jazz", "Nexus"],
      "word_count": 153
    }
  ],
  "statistics": {
    "total_files": 18,
    "total_words": 3388
  }
}
```

### 💡 主動創意建議系統

分析日誌模式，自動提供可執行的優化建議：

- **模式識別**: 實作/修復/優化/學習/設計
- **智能建議**: 基於使用習慣的具體建議
- **定期報告**: 每日/每週/每月報告
- **Cron 支援**: 自動排程執行

**使用:**
```bash
./scripts/idea-generator.sh
```

**輸出:**
```
📊 日誌分析統計
• 實作任務：5 次
• 修復問題：3 次
• 優化改進：3 次

💡 建議
1️⃣ 實作模式分析
   💡 建議：建立可重用組件庫
```

### 🔗 智能關聯分析系統

計算檔案之間的關聯關係，建立知識網絡：

- **6 種關係類型**: 強/中/弱/層次/版本/學習
- **關聯計算**: 基於關鍵詞共現、時間、主題
- **關聯網圖**: 生成 `memory/relations.json`

**使用:**
```bash
./scripts/relations-analyzer.sh
```

## 🗂️ 目錄結構

```
workspace/
├── SKILL.md              # 本文件
├── AGENTS.md             # Agent 行為規則
├── SOUL.md               # 身份與原則
├── MEMORY.md             # 長期記憶
├── NEXUS.md              # 記憶網絡樞紐
├── HEARTBEAT.md          # 自我檢查清單
├── TOOLS.md              # 工具配置
├── USER.md               # 用戶設定
├── WAL.md                # 操作日誌
├── EMOJI-JOURNAL.md      # 情緒溫度計
│
├── scripts/
│   ├── auto-index.sh     # 知識索引腳本
│   ├── idea-generator.sh # 創意建議腳本
│   └── relations-analyzer.sh  # 關聯分析腳本
│
├── docs/
│   ├── KNOWLEDGE-INDEX-ARCHITECTURE.md
│   ├── IDEA-SYSTEM-USAGE.md
│   ├── NEXUS-RELATIONS.md
│   └── IMPLEMENTATION-NOTES.md
│
└── memory/
    ├── index.json        # 知識索引
    ├── relations.json    # 關聯圖譜
    ├── heartbeat-state.json
    ├── daily/            # 每日記錄
    ├── lessons/          # 經驗教訓
    └── ideas/            # 創意想法
```

## 🚀 快速開始

### 1. 基礎設置

```bash
# 初始化目錄結構
mkdir -p memory/daily memory/lessons memory/ideas

# 建立每日日誌
echo "# $(date +%Y-%m-%d)" > memory/$(date +%Y-%m-%d).md
```

### 2. 執行系統

```bash
# 建立知識索引
./scripts/auto-index.sh

# 獲取創意建議
./scripts/idea-generator.sh

# (可選) 計算關聯
./scripts/relations-analyzer.sh
```

### 3. 自動排程

**每日 Heartbeat**:
```bash
# 添加到你的 Heartbeat 系統
./scripts/auto-index.sh > /dev/null 2>&1
```

**每週報告**:
```bash
# Crontab: 每週日早上 9 點
0 9 * * 0 cd /path/to/workspace && ./scripts/idea-generator.sh
```

## 📚 文檔

### 架構文件

- **[KNOWLEDGE-INDEX-ARCHITECTURE.md](docs/KNOWLEDGE-INDEX-ARCHITECTURE.md)** - 知識索引系統設計
- **[IDEA-SYSTEM-USAGE.md](docs/IDEA-SYSTEM-USAGE.md)** - 創意建議系統使用指南
- **[NEXUS-RELATIONS.md](docs/NEXUS-RELATIONS.md)** - 關聯分析系統規格 (6 種關係)
- **[IMPLEMENTATION-NOTES.md](docs/IMPLEMENTATION-NOTES.md)** - 實作記錄

### 核心文件

- **[AGENTS.md](AGENTS.md)** - Agent 行為規則與路由
- **[NEXUS.md](NEXUS.md)** - 記憶網絡樞紐
- **[MEMORY.md](MEMORY.md)** - 長期記憶管理
- **[HEARTBEAT.md](HEARTBEAT.md)** - 主動巡檢機制

## 🔄 工作流程

```
1. 每日寫日誌
   └─> memory/YYYY-MM-DD.md

2. 自動索引更新
   └─> ./scripts/auto-index.sh
   └─> memory/index.json

3. 創意建議生成
   └─> ./scripts/idea-generator.sh
   └─> idea-suggestions.txt

4. 關聯分析
   └─> ./scripts/relations-analyzer.sh
   └─> memory/relations.json

5. 定期回顧
   └─> 每週/每月彙整到 MEMORY.md
```

## 🔧 進階使用

### 自訂關鍵詞

編輯 `scripts/idea-generator.sh`:

```bash
# 添加你的關鍵詞
your_keyword=$(grep -rc '你的關鍵詞' "$LOG_DIR")
```

### Cron 自動執行

```bash
# 每日 9 點生成建議
0 9 * * * cd ~/workspace && ./scripts/idea-generator.sh >> weekly.log

# 每週日全量索引
0 8 * * 0 cd ~/workspace && ./scripts/auto-index.sh
```

### Git 集成

```bash
# 提交前生成報告
./scripts/idea-generator.sh > .commit-report.md
git add . && git commit -F .commit-report.md
```

## 🎯 使用場景

### 場景 1: 個人知識管理
- 每日記錄 → 自動索引 → 每週回顧
- 自動識別知識盲點

### 場景 2: 專案管理
- 追蹤實作/修復/優化比例
- 自動建議改進方向

### 場景 3: Agent 協作
- 路由決策 → 執行 → 記錄
- 自動總結經驗教訓

## 📊 統計數據

**本框架特性:**

| 功能 | 文件數 | 字數 | 狀態 |
|------|--------|------|------|
| 知識索引 | 18+ | 3,388 | ✅ |
| 創意建議 | 3 腳本 | 2,341 | ✅ |
| 關聯分析 | 4 文件 | 4,401 | ✅ |
| 使用文檔 | 1 文件 | 6,000+ | ✅ |

## 🌟 最佳實踐

1. **每日記錄**: 在 `memory/YYYY-MM-DD.md` 寫日誌
2. **每週回顧**: 執行建議系統，整理教訓
3. **每月沉澧**: 將重要決策寫到 `MEMORY.md`
4. ** Git 提交**: 記錄架構變更和決策

## 📄 許可證

**MIT-0** - 免費使用，修改，重新分發。無需署名。

## 🙏 致敬

感謝所有 OpenClaw 社區成員與貢獻者。

---

**版本**: 2.0.0  
**最後更新**: 2026-03-25  
**作者**: [@lalawgwg99](https://github.com/lalawgwg99)
