---
name: integrated-memory-evolution-action
description: "整合三層記憶系統 + 自進化引擎 + 行動模式。所有 Agent 必須使用的核心 Skill，實現記憶驅動、自進化、主動行動的完整閉環。"
metadata: { "openclaw": { "emoji": "🧠⚡🎯" } }
version: 1.0.0
tags: ["memory", "evolution", "action", "mandatory", "core"]
---

# 🧠⚡🎯 Integrated Memory Evolution Action (整合記憶進化行動)

**所有 Agent 必須使用！** 整合咗：
- 🧠 **三層記憶系統**（Layer 1/2/3）
- ⚡ **自進化引擎**（T130 四個核心技能）
- 🎯 **行動模式**（Proactive Agent 架構）

---

## 🎯 核心目標

建立一個**記憶驅動、自進化、主動行動**的完整閉環系統：

```
┌─────────────────────────────────────────────────────────┐
│  記憶層（Memory Layer）                                   │
│  - Layer 1: 對話總結（即時）                              │
│  - Layer 2: 事件記錄（任務/錯誤/財務/技能）               │
│  - Layer 3: 永久記憶（用戶習慣/API 配置/原則）            │
└────────────────────┬────────────────────────────────────┘
                     ▼ 記憶驅動決策
┌─────────────────────────────────────────────────────────┐
│  進化層（Evolution Layer）                                │
│  - 學習記錄（LEARNINGS.md）                              │
│  - 錯誤追蹤（ERRORS.md）                                 │
│  - 功能請求（FEATURE_REQUESTS.md）                       │
│  - 實驗驅動（EXPERIMENTS.md）                            │
│  - 本體圖譜（ontology/graph.jsonl）                      │
└────────────────────┬────────────────────────────────────┘
                     ▼ 進化驅動優化
┌─────────────────────────────────────────────────────────┐
│  行動層（Action Layer）                                   │
│  - WAL Protocol（寫入先過行動）                          │
│  - Working Buffer（危險區記錄）                          │
│  - Autonomous Crons（自動化任務）                        │
│  - Resourcefulness（嘗試 10 種方法）                      │
│  - Compaction Recovery（上下文恢復）                     │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 強制使用流程

### 1️⃣ 任務前檢查（Pre-Task Check）- **必須執行**

每次接任務/對話前必須執行以下步驟：

```markdown
## 任務前檢查清單

### 記憶層檢查
- [ ] 讀取 Layer 3（用戶習慣、核心規則）
  - 位置：`/shared/memory/layer3-permanent/user-profile.md`
  - 重點：溝通風格、工作習慣、禁忌清單
  
- [ ] 讀取 Layer 2（任務狀態、犯錯記錄）
  - 位置：`/shared/memory/layer2-events/tasks/`
  - 重點：當前任務、相關錯誤記錄
  
- [ ] 讀取 Layer 1（今日對話）
  - 位置：`/shared/memory/layer1-conversations/YYYY-MM-DD/`
  - 重點：今日相關對話總結
  
- [ ] 執行 memory_search
  - 命令：`memory_search query="<關鍵詞>"`
  - 重點：搜索相關記憶片段

### 進化層檢查
- [ ] 讀取 `.learnings/LEARNINGS.md`
  - 位置：`workspace/.learnings/LEARNINGS.md`
  - 重點：相關學習記錄
  
- [ ] 讀取 `.learnings/ERRORS.md`
  - 位置：`workspace/.learnings/ERRORS.md`
  - 重點：避免重複犯錯
  
- [ ] 讀取本體圖譜（如需要）
  - 位置：`memory/ontology/graph.jsonl`
  - 重點：實體關係查詢

### 行動層檢查
- [ ] 讀取 `SESSION-STATE.md`
  - 位置：`workspace/SESSION-STATE.md`
  - 重點：當前工作狀態、WAL 目標
  
- [ ] 檢查 `HEARTBEAT.md`
  - 位置：`workspace/HEARTBEAT.md`
  - 重點：待辦任務清單

**未檢查前唔好行動！**
```

---

### 2️⃣ 對話中記錄（WAL Protocol）- **必須執行**

**Write-Ahead Log：** 寫入記憶 **先過** 回覆！

#### 記憶層寫入

| 觸發情況 | 即時寫入邊層 | 寫入位置 |
|----------|-------------|----------|
| CEO 給出決策 | Layer 2 | `/shared/memory/layer2-events/tasks/` |
| CEO 表達偏好 | Layer 3 | `/shared/memory/layer3-permanent/user-profile.md` |
| CEO 分配任務 | Layer 2 | `/shared/memory/layer2-events/tasks/Txxx.md` |
| CEO 指出錯誤 | Layer 2 | `/shared/memory/layer2-events/errors/` |
| CEO 提供信息 | Layer 1 | `/shared/memory/layer1-conversations/YYYY-MM-DD/` |
| 任務完成 | Layer 2 | 更新任務狀態 |
| 技能使用 | Layer 2 | `/shared/memory/layer2-events/skills/` |

#### 進化層寫入

| 觸發情況 | 寫入文件 | ID 格式 |
|----------|---------|---------|
| 學到新嘢 | `.learnings/LEARNINGS.md` | `LRN-YYYYMMDD-XXX` |
| 犯咗錯誤 | `.learnings/ERRORS.md` | `ERR-YYYYMMDD-XXX` |
| 發現需求 | `.learnings/FEATURE_REQUESTS.md` | `FEAT-YYYYMMDD-XXX` |
| 實驗結果 | `.learnings/EXPERIMENTS.md` | `EXP-YYYYMMDD-XXX` |
| 新實體/關係 | `memory/ontology/graph.jsonl` | JSONL 格式 |

#### 行動層寫入

| 觸發情況 | 寫入位置 | 內容 |
|----------|---------|------|
| 開始任務 | `SESSION-STATE.md` | 任務目標、進度 |
| 遇到阻礙 | `memory/working-buffer.md` | 危險區記錄、嘗試方法 |
| 完成行動 | `SESSION-STATE.md` | 結果、下一步 |

---

### 3️⃣ 對話後寫入（Post-Dialogue Write）- **必須執行**

#### 記憶層歸檔

```bash
# 1. 更新 Layer 1（對話總結）
# 位置：/shared/memory/layer1-conversations/YYYY-MM-DD/<agent>.md

# 2. 更新 Layer 2（任務狀態）
# 位置：/shared/memory/layer2-events/tasks/Txxx.md

# 3. 更新 Layer 3（如有需要）
# 位置：/shared/memory/layer3-permanent/user-profile.md
```

#### 進化層歸檔

```bash
# 1. 記錄學習
node scripts/log-learning.mjs learning "摘要" "詳情" "建議行動"

# 2. 記錄錯誤
node scripts/log-learning.mjs error "摘要" "錯誤詳情" "建議修復"

# 3. 記錄本體（如需要）
python3 scripts/ontology.py create --type Task --props '{"title":"任務名","status":"open"}'
```

#### 行動層歸檔

```bash
# 1. 更新 SESSION-STATE.md
# - 更新任務進度
# - 記錄下一步行動

# 2. 清理 working-buffer.md
# - 移動已完成到 SESSION-STATE.md
# - 保留進行中項目
```

---

## 🔄 自進化循環

### 每日流程（00:00）

```
┌─────────────────────────────────────────────────────────┐
│  1. 收集 Layer 1 對話總結                                 │
│     - 位置：/shared/memory/layer1-conversations/YYYY-MM-DD/ │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  2. 提煉到 Layer 2                                       │
│     - 任務 → layer2-events/tasks/                       │
│     - 錯誤 → layer2-events/errors/                      │
│     - 技能 → layer2-events/skills/                      │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  3. 記錄到進化層                                         │
│     - 學習 → .learnings/LEARNINGS.md                    │
│     - 錯誤 → .learnings/ERRORS.md                       │
│     - 本體 → memory/ontology/graph.jsonl                │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  4. 優化行動層                                           │
│     - 更新 SESSION-STATE.md                             │
│     - 更新 HEARTBEAT.md                                 │
│     - 優化 AGENTS.md/TOOLS.md                           │
└─────────────────────────────────────────────────────────┘
```

### 每週流程（週日 23:00）

```
┌─────────────────────────────────────────────────────────┐
│  1. 檢視 .learnings/ 文件                                │
│     - 識別重複錯誤                                       │
│     - 提煉核心學習                                       │
│     - 晉升到 AGENTS.md/TOOLS.md                         │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  2. 檢視本體圖譜                                         │
│     - 識別孤立實體                                       │
│     - 建立新關係                                         │
│     - 優化 schema.yaml                                  │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  3. 檢視行動模式                                         │
│     - 優化 WAL Protocol                                 │
│     - 更新 Working Buffer 規則                           │
│     - 調整 Autonomous Crons                             │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 健康檢查指標

### 記憶層健康

| 指標 | 目標 | 檢查頻率 | 驗證命令 |
|------|------|----------|----------|
| Layer 1 更新 | 每次對話 | 實時 | `ls -lht layer1-conversations/` |
| Layer 2 分類 | 5 類完整 | 每日 | `ls layer2-events/` |
| Layer 3 文件 | >0 | 每週 | `cat layer3-permanent/*.md` |
| memory_search | <3 秒 | 按需 | `memory_search query="test"` |

### 進化層健康

| 指標 | 目標 | 檢查頻率 | 驗證命令 |
|------|------|----------|----------|
| LEARNINGS.md | >0/週 | 每週 | `cat .learnings/LEARNINGS.md` |
| ERRORS.md | 0 重複 | 每日 | `grep "重複" .learnings/ERRORS.md` |
| 本體圖譜 | >10 實體 | 每週 | `wc -l memory/ontology/graph.jsonl` |
| 知識晉升 | >1/月 | 每月 | `grep "晉升" .learnings/LEARNINGS.md` |

### 行動層健康

| 指標 | 目標 | 檢查頻率 | 驗證命令 |
|------|------|----------|----------|
| SESSION-STATE.md | 更新 <2h | 每 2h | `ls -lht SESSION-STATE.md` |
| Working Buffer | 清空 <24h | 每日 | `cat memory/working-buffer.md` |
| WAL Protocol | 100% 執行 | 每次對話 | `grep "WAL" layer1-conversations/` |
| Resourcefulness | 嘗試>3 種 | 每次任務 | `grep "嘗試" working-buffer.md` |

---

## 🚨 違規處理

### 記憶層違規

| 違規 | 處理 |
|------|------|
| 未讀取 Layer 3 就行動 | 警告 + 補讀取 |
| 未寫入 Layer 1 | 警告 + 補記錄 |
| 重複犯同一錯誤 | 重啟 + 記錄教訓 |
| 失憶（唔記得之前講過） | 降級權限 + 通知 CEO |

### 進化層違規

| 違規 | 處理 |
|------|------|
| 未記錄學習 | 警告 + 補記錄 |
| 未記錄錯誤 | 警告 + 記錄教訓 |
| 本體圖譜未更新 | 警告 + 補實體 |
| 知識未晉升 | 提醒 + 安排晉升 |

### 行動層違規

| 違規 | 處理 |
|------|------|
| 未執行 WAL Protocol | 警告 + 補寫入 |
| Working Buffer 超時 | 警告 + 清理 |
| 未嘗試 3 種方法就求助 | 提醒 + 繼續嘗試 |
| SESSION-STATE 未更新 | 警告 + 補更新 |

---

## 📝 模板文件

### Layer 1 對話記錄模板

```markdown
# YYYY-MM-DD [Agent 名] 對話記錄

## HH:MM - [主題]

**參與者：** CEO, [Agent]
**關鍵內容：**
- [要點 1]
- [要點 2]

**提取記憶：**
- **任務：** [Txxx]
- **錯誤：** [如有]
- **學習：** [如有]
- **習慣：** [如有]

**寫入位置：**
- Layer 1: ✅ 已寫入
- Layer 2: ✅ 已寫入（如適用）
- Layer 3: ✅ 已寫入（如適用）
```

### Layer 2 任務記錄模板

```markdown
# [任務 ID] [任務名稱]

**創建：** YYYY-MM-DD
**負責：** [Agent]
**狀態：** 🔄 進行中 / ✅ 完成 / ❌ 失敗

## 目標
[任務目標]

## 進度
- [ ] 步驟 1
- [ ] 步驟 2

## 結果
*完成後填寫*

## 教訓
*完成後填寫*
```

### 學習記錄模板

```markdown
## LRN-YYYYMMDD-XXX - [學習主題]

**日期：** YYYY-MM-DD
**來源：** [對話/任務/錯誤]

**摘要：**
[一句話總結]

**詳情：**
[詳細描述]

**建議行動：**
[具體行動建議]

**晉升狀態：** ⏳ 待晉升 / ✅ 已晉升到 [文件]
```

### 錯誤記錄模板

```markdown
## ERR-YYYYMMDD-XXX - [錯誤主題]

**日期：** YYYY-MM-DD
**嚴重性：** 🔴 高 / 🟡 中 / 🟢 低

**摘要：**
[一句話總結]

**錯誤詳情：**
[詳細描述]

**建議修復：**
[具體修復方案]

**重複檢測：** ⚠️ 重複 / ✅ 首次
**相關錯誤：** [見 ERR-YYYYMMDD-YYY]
```

---

## 🛠️ 工具命令

### 記憶層命令

```bash
# 搜索記憶
memory_search query="<關鍵詞>"

# 讀取 Layer 3
cat /shared/memory/layer3-permanent/user-profile.md

# 讀取 Layer 2 任務
cat /shared/memory/layer2-events/tasks/Txxx.md

# 讀取 Layer 1
cat /shared/memory/layer1-conversations/YYYY-MM-DD/<agent>.md
```

### 進化層命令

```bash
# 記錄學習
node scripts/log-learning.mjs learning "摘要" "詳情" "建議行動"

# 記錄錯誤
node scripts/log-learning.mjs error "摘要" "錯誤詳情" "建議修復"

# 創建本體實體
python3 scripts/ontology.py create --type Task --props '{"title":"任務名","status":"open"}'

# 查詢本體
python3 scripts/ontology.py query --type Task --where '{"status":"open"}'

# 建立關係
python3 scripts/ontology.py relate --from proj_001 --rel has_task --to task_001
```

### 行動層命令

```bash
# 更新 SESSION-STATE
edit SESSION-STATE.md

# 更新 Working Buffer
edit memory/working-buffer.md

# 檢查 HEARTBEAT
cat HEARTBEAT.md
```

---

## 📚 參考文件

### 核心文件
- `AGENTS.md` - 運營規則
- `SOUL.md` - 身份原則
- `USER.md` - 用戶上下文
- `MEMORY.md` - 長期記憶
- `HEARTBEAT.md` - 週期性自檢

### 記憶層文件
- `/shared/memory/layer1-conversations/` - 對話總結
- `/shared/memory/layer2-events/` - 事件記錄
- `/shared/memory/layer3-permanent/` - 永久記憶

### 進化層文件
- `.learnings/LEARNINGS.md` - 學習記錄
- `.learnings/ERRORS.md` - 錯誤記錄
- `.learnings/FEATURE_REQUESTS.md` - 功能請求
- `.learnings/EXPERIMENTS.md` - 實驗記錄
- `memory/ontology/graph.jsonl` - 本體圖譜
- `memory/ontology/schema.yaml` - 類型定義

### 行動層文件
- `SESSION-STATE.md` - 主動工作記憶
- `memory/working-buffer.md` - 危險區日誌

---

## 🎯 快速開始

**新 Agent 首次使用：**

1. **讀取核心文件**
   ```bash
   cat AGENTS.md SOUL.md USER.md
   ```

2. **讀取記憶層**
   ```bash
   cat /shared/memory/layer3-permanent/user-profile.md
   cat /shared/memory/layer2-events/tasks/
   cat /shared/memory/layer1-conversations/$(date +%Y-%m-%d)/
   ```

3. **讀取進化層**
   ```bash
   cat .learnings/{LEARNINGS,ERRORS,FEATURE_REQUESTS,EXPERIMENTS}.md
   cat memory/ontology/graph.jsonl
   ```

4. **讀取行動層**
   ```bash
   cat SESSION-STATE.md
   cat memory/working-buffer.md
   cat HEARTBEAT.md
   ```

5. **開始行動（跟從 WAL Protocol）**

---

**最後更新：** 2026-04-05 07:10  
**維護：** 所有 Agent（每次對話必須使用）  
**版本：** v1.0
