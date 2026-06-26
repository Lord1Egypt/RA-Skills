---
name: memory-fusion-lite
description: "Memory Fusion Light — 基于 dztabel-happy/openclaw-memory-fusion 核心思想：三层 cron 自动记忆提取/滚动蒸馏/防套娃。功能：①A′滚动7天区 ②增量扫描脚本 ③防套娃三保险 ④每周分类治理。适用已部署 Dreaming 的用户补强记忆闭环。"
license: MIT
version: 2026.4.16
---

# 🧠 Memory Fusion Lite

基于 [dztabel-happy/openclaw-memory-fusion](https://github.com/dztabel-happy/openclaw-memory-fusion) 核心思想重构，保留最有价值的三部分，轻量集成到现有 Dreaming 系统。

## 核心价值

| 来自 memory-fusion | 在本 skill 中的实现方式 |
|-------------------|----------------------|
| Byte offset 增量扫描 | `scan_sessions_incremental.py`（原生脚本） |
| A′ 滚动7天区 | Dreaming L2 phase 自动写 MEMORY.md 末尾滚动区 |
| 防套娃三保险 | 扫描器忽略规则 + prompt 前缀 + 收敛验证 |
| 每周分类治理 | Weekly cron job 执行晋升/剪枝/归档 |

## 架构概览

```
session JSONL
    │
    ├── Dreaming（每晚 3am）
    │   └── DREAMS.md + memory/dreaming/
    │
    ├── memory-fusion-lite L2（每天 23:30）
    │   └── scan_sessions_incremental.py（增量）
    │         → LLM 提炼 → MEMORY.md#A′ 滚动区（≤30条）
    │
    └── memory-fusion-lite L3（每周一 00:20）
          └── LLM 扫描 A′ → 晋升1-2条 → weekly 归档
```

## 安装前检查

### 1. Dreaming 必须已启用

检查 `plugins.entries.memory-core.config.dreaming.enabled === true`

### 2. memory/_state/ 目录已创建

```bash
mkdir -p ~/.openclaw/workspace/memory/_state
```

### 3. memory/weekly/ 目录已创建

```bash
mkdir -p ~/.openclaw/workspace/memory/weekly
```

## 文件清单

### 核心脚本

- `scripts/scan_sessions_incremental.py` — **增量扫描脚本**（来自 memory-fusion 原始仓库，618行 Python3）

### 必读参考文档

1. `references/a-prime-zone.md` — A′ 滚动7天区格式规范与维护规则
2. `references/anti-recursion.md` — 防套娃三保险实现细节
3. `references/weekly-governance.md` — 每周分类治理流程

### 可选参考

- `references/diff-from-dreaming.md` — 与 Dreaming 的分工边界说明

## 触发条件

**自动触发（cron）：**

| 层级 | 名称 | cron 表达式 | 内容 |
|------|------|------------|------|
| L2 | memory-fusion-lite daily | `30 23 * * *`（Asia/Shanghai） | 增量扫描 → LLM 提炼 → A′ 区写入 |
| L3 | memory-fusion-lite weekly | `20 0 * * 1`（Asia/Shanghai） | A′ 区分类治理 + 晋升 + 归档 |

**手动触发：**
- `/memory-fusion-lite daily` — 立即执行 L2 daily
- `/memory-fusion-lite weekly` — 立即执行 L3 weekly
- `/memory-fusion-lite status` — 查看各层执行状态

## L2 执行流程（增量扫描管道）

```
1. 运行脚本
   python3 scripts/scan_sessions_incremental.py \
     --openclaw-dir /root/.openclaw \
     --agent main \
     --format md \
     --max-messages 50

2. 脚本输出（markdown）→
   ## session-xxxx
   - U: user 消息
   - A: assistant 最终回复（不含tool_calls）

3. LLM 提炼（忽略 cron/NO_REPLY/System 消息）

4. 写 MEMORY.md A′ 区
   - 每天最多5条
   - 总数超30条时删除最老条目
   - 更新 "上次清理" 注释
```

## A′ 滚动7天区（核心）

### 格式

在 `MEMORY.md` 末尾维护一个独立章节：

```markdown
## 近期重要更新（自动，滚动7天）

<!-- A′ zone: auto-maintained by memory-fusion-lite -->
<!-- 规则：≤30条，每天最多新增5条，每周晋升1-2条到上方分类区 -->
<!-- 上次清理：2026-04-15 -->

## 2026-04-15
- **主题**：简短描述
```

### 维护规则

1. **条目上限**：≤30条，超出时删除最老的
2. **每日新增**：每天 L2 最多加5条
3. **每周晋升**：L3 把"已证实且长期有效"的条目晋升到 MEMORY.md 的主分类区
4. **时间窗口**：滚动7天

## 防套娃三保险

### 第一保险：prompt 前缀

所有 cron prompt 第一行必须是：

```
[cron:memory-daily] ...  (L2)
[cron:memory-weekly] ... (L3)
```

### 第二保险：扫描器忽略规则

`scan_sessions_incremental.py` 自动忽略：
- 首条 user 消息以 `[cron:` 开头的 session（`_classify_is_cron_session`）
- 内容含 `memory-daily ok` / `memory-weekly ok` / `NO_REPLY` 的消息
- `tool` / `system` role 的消息

### 第三保险：收敛验证

脚本统计 `messages_emitted` 和 `messages_ignored`，当 `ignored >> emitted` 时说明过滤器在正常工作。

## 状态文件

| 文件 | 内容 |
|------|------|
| `memory/_state/scan_sessions_incremental.json` | **字节偏移游标**（脚本自带） |
| `memory/_state/last-daily.json` | L2 上次执行时间戳 |
| `memory/_state/last-weekly.json` | L3 上次执行时间戳 + ISO week |
| `memory/_state/weekly-gate.json` | 本周是否已执行 flag |

## 与 Dreaming 的分工

| | Dreaming | memory-fusion-lite |
|---|---|---|
| 触发 | 每晚 3am | L2 23:30 / L3 周一 00:20 |
| 重点 | 语义理解 + 记忆整理 | 增量扫描 + 滚动更新 + 分类治理 |
| 输出 | DREAMS.md + phase reports | MEMORY.md A′ 区 + weekly 归档 |
| 扫描方式 | 全量 session | **增量**（字节偏移游标） |

**两者互补，不冲突。Dreaming 保留，本 skill 补强。**

## 依赖

- Dreaming 已启用（`plugins.entries.memory-core.config.dreaming.enabled === true`）
- Python3 环境（用于运行 scan_sessions_incremental.py）
- memory/ 目录存在且可写
- memory/_state/ 目录存在
- memory/weekly/ 目录存在

## 不包含的内容

以下 memory-fusion 功能**未包含**：

- 独立三层 cron 系统（与 Dreaming 重复）→ 复用 Dreaming cron 管道
- Telegram 通知面板（未配置）
- QMD embedding 变更（已有 Ollama）

## 升级

```
openclaw skills update memory-fusion-lite
```
