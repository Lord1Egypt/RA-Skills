# NEXUS-RELATIONS.md — 知識關聯系統規格

## 🎯 核心概念

Nexus Framework 的知識關聯網絡，將所有記憶、文件、決策連接成網狀結構。

## 📐 關聯類型 (6 種)

### 1. 強連接 (Strength: 1.0)
**定義**: 同一主題核心文件
**例子**:
- `MEMORY.md` ↔ `NEXUS.md` (記憶系統核心)
- `AGENTS.md` ↔ `SOUL.md` (代理行為核心)
- `scripts/auto-index.sh` ↔ `docs/KNOWLEDGE-INDEX-ARCHITECTURE.md`

### 2. 中連接 (Strength: 0.6)
**定義**: 共用 3+ 個關鍵詞或相似標題結構
**例子**:
- `memory/2026-03-24.md` ↔ `MEMORY.md` (都提到 Nexus 整合)
- `AGENTS.md` ↔ `EMOJI-JOURNAL.md` (都涉及溝通風格)

### 3. 弱連接 (Strength: 0.3)
**定義**: 時間相關 (±7 天) 或相關主題
**例子**:
- `memory/2026-03-22.md` ↔ `memory/2026-03-24.md` (±2 天的日誌)
- `memory/2024-03-24.md` ↔ `SCRIPTS/auto-index.sh` (開發日誌 ↔ 腳本)

### 4. 層次連接 (Strength: 0.8)
**定義**: 架構层级關係
**例子**:
- `docs/KNOWLEDGE-INDEX-ARCHITECTURE.md` (架構) → `scripts/auto-index.sh` (實作)
- `NEXUS.md` (規範) → `memory/heartbeat-state.json` (執行)

### 5. 版本連接 (Strength: 0.5)
**定義**: 文件更新歷史
**例子**:
- `AGENTS.md` v1.0 → `AGENTS.md` v2.0

### 6. 學習連接 (Strength: 0.7)
**定義**: 經驗教訓 → 對應文件
**例子**:
- `memory/lessons/` → `NEXUS.md` (教訓更新規範)

## 🔢 關聯計算算法

### 1. 共現分析 (Keyword Co-occurrence)
```bash
相似度 = (共同關鍵詞數) / min(文件 A 關鍵詞數，文件 B 關鍵詞數)
```

### 2. 時間關聯 (Temporal)
```bash
連接強度 = max(0, 1 - (天數差異 / 14))
# ±7 天內：0.5-1.0
# 7-14 天：0.3-0.5
# 超過 14 天：0.3
```

### 3. 主題匹配 (Semantic)
```bash
主觀評分 (0.8-1.0) 或 自動判斷 (0.3-0.7)
```

## 🛠️ API 設計

### 關聯查詢 API
```json
POST /api/relations
{
  "file": "memory/2026-03-24.md",
  "depth": 2,
  "min_strength": 0.3
}

Response:
{
  "relations": [
    {
      "to": "MEMORY.md",
      "type": "strong",
      "strength": 0.85,
      "shared_keywords": ["memory", "長期", "沉澱"],
      "reason": "共現分析 + 主题匹配"
    }
  ]
}
```

## 📊 權重系統

| 類型 | 強度 | 計算方式 | 用途 |
|------|------|---------|------|
| 強連接 | 1.0 | 核心主題共用 | 知識導航 |
| 中連接 | 0.6 | 關鍵詞共現 (3+) | 相關建議 |
| 弱連接 | 0.3 | 時間相關 | 時間線瀏覽 |
| 層次連接 | 0.8 | 架構關係 | 上層視圖 |
| 版本連接 | 0.5 | 更新歷史 | 變更追蹤 |
| 學習連接 | 0.7 | 教訓映射 | 經驗回溯 |

## 🔄 自動更新機制

### 1. 事件驅動
- **寫入日誌**: 立即更新 `memory/index.json`
- **修改核心文件**: 即時重新計算關聯
- **每日 Heartbeat**: 全量掃描 + 增量更新

### 2. 觸發條件
```yaml
觸發條件:
  - 新增文件: 立即計算
  - 修改文件: 增量更新
  - 沉澧到 MEMORY.md: 全量重新計算
  - 每週日 02:00: 定期維護
```

## 💡 使用場景

### 1. 知識導航
```
當前文件: memory/2026-03-24.md
→ 相關文件: MEMORY.md (0.85), NEXUS.md (0.72)
→ 建議: 查看長期記憶沉淀進度
```

### 2. 模式識別
```
分析: 本週 3 次提到"API 限流"
→ 相關文件: TOOLS.md, AGENTS.md
→ 建議: 建立更完善的 fallback 機制
```

### 3. 決策回顧
```
決策: 使用 Mimo-V2-Flash 作為備用模型
→ 相關文件: MEMORY.md, NEXUS.md
→ 教訓: [記錄到記憶教訓區]
```

## 📁 目錄結構

```
memory/
├── index.json              # 完整知識網絡索引
├── relations.json          # 關聯圖譜
├── daily/                  # 每日記錄
├── lessons/                # 經驗教訓
├── ideas/                  # 創意想法
└── heartbeat-state.json    # 心跳狀態

docs/
├── NEXUS-RELATIONS.md      # 本文件
├── KNOWLEDGE-INDEX-ARCHITECTURE.md
└── IDEA-GENERATOR-ARCHITECTURE.md
```

## 🚀 下一步實現

### Phase 1: 基礎建設 (3-5 天)
- [ ] 檔案監聽器 (chokidar)
- [ ] 共現分析模組
- [ ] 基本索引系統

### Phase 2: 語義層 (5-7 天)
- [ ] 向量引擎集成 (可選)
- [ ] 自動標籤建議
- [ ] 知識地圖可視化

### Phase 3: 自動優化 (長期)
- [ ] 學習連接自動發現
- [ ] 關聯強度自我調整
- [ ] 異常關聯偵測

