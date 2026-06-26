---
name: openclaw-memory-system
description: OpenClaw 记忆管理系统，三层架构（NOW.md + 每日日志 + 知识库），支持 heartbeat 写入、夜间反思、CRUD 验证、主动遗忘。Based on Ray Wang's 30-day production experience.
---

# OpenClaw Memory System v1.0

基于 Ray Wang 的生产实践经验，30天迭代的记忆管理系统。

## 核心原则

**文件 = 事实来源**
- Context Window 是工作台，文件才是仓库
- 不写进文件的东西 = 你从来不知道的东西

## 三层架构

### 1. 短期层：NOW.md
- 用途：Agent 的"工作台"，当前状态、优先级、阻塞项
- 特点：覆写式（每次 heartbeat 更新）
- 位置：`~/.openclaw/workspace/NOW.md`

### 2. 中期层：memory/YYYY-MM-DD.md
- 用途：事件流水，记录当天发生的一切
- 特点：追加式，永不覆写
- 位置：`~/.openclaw/workspace/memory/`

### 3. 长期层：INDEX.md → 结构化知识库
- 用途：提炼后的可复用知识
- 目录：lessons/、decisions/、people/、projects/、preferences/
- 位置：`~/.openclaw/workspace/memory/INDEX.md`

## 目录结构

```
workspace/
├── NOW.md                  # 短期：状态仪表盘（覆写式）
├── MEMORY.md               # 指向 INDEX.md 的指针
├── AGENTS.md               # Agent 操作手册
├── HEARTBEAT.md            # Heartbeat 执行流程
│
└── memory/
    ├── INDEX.md            # 知识导航（启动时必读）
    ├── YYYY-MM-DD.md       # 每日日志（追加式）
    │
    ├── decisions/          # 战略决策记录
    ├── lessons/            # 可复用教训
    ├── people/             # 人物画像
    ├── projects/           # 项目状态
    ├── preferences/        # 用户偏好
    ├── reflections/        # 每日自省
    ├── actions/            # 任务卡片
    │
    └── .archive/           # 冷存储（不索引）
```

## Frontmatter 规范

```yaml
---
title: "主题"
date: 2026-03-24
category: lessons|person|decision
priority: 🔴|🟡|⚪
status: active|superseded|conflict
last_verified: 2026-03-24
tags: []
---
```

## 状态流转

```
active ──→ superseded    (被更新版本取代)
active ──→ conflict      (发现矛盾信息，待人工裁决)
conflict ──→ active      (人工裁决后恢复)
```

## 生命周期

### 日间（Heartbeat 每 30-60 分钟）
1. 扫描活跃 session 消息
2. 提取重要信息写入日志
3. 路由到对应知识文件（轻量去重）
4. 刷新 NOW.md

### 23:30 日志同步
- 扫描全天所有 session 补漏

### 23:45 夜间反思
1. 读取上下文（今日日志 + NOW.md + 相关知识文件）
2. 写反思（计划 vs 实际 + 教训 + 明天改变）
3. 清理日志（去重）
4. **CRUD 回写知识库** ← 核心
5. 过时扫描（>30 天标记 [⚠️ STALE]）

### 每周日 00:00 GC 归档
- 日志 >30 天 + 无引用 → .archive/
- 反思 >30 天 → 归档
- 核心知识（decisions/、lessons 🔴、people/）永不归档

## 温度模型

| 温度 | 状态 | 处理 |
|------|------|------|
| T > 0.7 | 🔥 Hot | 保持活跃索引 |
| 0.3 < T ≤ 0.7 | 🌤️ Warm | 保留但检索降权 |
| T ≤ 0.3 | 🧊 Cold | 移至 .archive/ |

```
Temperature = w_age × age_score + w_ref × ref_score + w_pri × priority_score
```

## 写入工具

| 工具 | 用途 | 场景 |
|------|------|------|
| `memlog.sh "Title" "Body"` | 日记追加 | 事件、完成、决策 |
| `Write NOW.md` | 覆写 | **仅** NOW.md |
| `printf >> file` | 追加 | lessons/ people/ 等 |

## 写入禁忌

- ❌ 硬编码时间戳（用脚本自动取）
- ❌ 用 Edit 修改 memory/ 文件
- ❌ 用 Write 覆写已有 memory/ 文件
- ❌ 写无实质内容的噪音
- ❌ 不读就写知识文件

## 检索策略

### L1: 扫 INDEX.md → 定位目标文件
- 适用：知道要找什么类别

### L2: 直接读取目标文件
- 适用：已知具体文件路径

### L3: QMD 语义搜索
- 适用：不确定信息在哪个文件

## CRUD 验证

写入知识文件时必须：

1. **READ** - 读取目标文件当前内容
2. **COMPARE** - 比较新知识与已有内容
   - 已有覆盖新知识 → NOOP (跳过)
   - 新知识更新 → UPDATE (旧版标记 superseded)
   - 新知识矛盾 → CONFLICT (两版保留 + 标记)
   - 全新的知识 → ADD (追加)
3. **METADATA** - 更新 last_verified 日期

## 记忆幻觉防护

| 类型 | 描述 | 例子 |
|------|------|------|
| 编造 | 写入从未发生过的事情 | Agent 声称"昨天做了 X" |
| 错误 | 写入不准确的信息 | 把 A 的观点归因给 B |
| 冲突 | 同一事实的两个矛盾版本并存 | 说"用方案 A"又说"用方案 B" |
| 遗漏 | 重要信息没有被记录 | 关键决策没写进文件 |

## 快速上手（最小配置）

```yaml
workspace/
├── NOW.md           # 状态板
├── AGENTS.md        # Agent 操作手册
└── memory/
    └── YYYY-MM-DD.md  # 每日日志
```

## Obsidian 集成

将 memory/ 目录设为 Obsidian vault：
- 启用核心插件：File explorer、Graph view、Backlinks、Daily notes
- 设置 useMarkdownLinks: false，启用 [[wiki-link]]
- 开启"显示隐藏文件"浏览归档

## 设计灵感

- 人脑记忆整合（睡眠时整合）
- 艾宾浩斯遗忘曲线
- Stanford Generative Agents
- Mem0 / MemGPT / HaluMem
