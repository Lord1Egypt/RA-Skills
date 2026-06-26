# Memory Sync CN

记忆同步系统 - 自动同步 OpenClaw 记忆系统与 CortexGraph。

## 功能

- 🔄 **双向同步**: MEMORY.md ↔ CortexGraph
- 🧠 **遗忘曲线**: 基于 Ebbinghaus 的智能记忆管理
- 📊 **自动晋升**: 高价值记忆自动升级到长期存储
- 🔍 **智能检索**: 语义搜索 + 衰减评分

## 安装

```bash
# 安装 CortexGraph
uv tool install cortexgraph

# 安装 mcporter
npm install -g mcporter

# 配置 CortexGraph
mcporter config add cortexgraph --command "$(which cortexgraph)"
```

## 使用

### 同步 MEMORY.md

```bash
./scripts/sync-memory.sh
```

### 同步每日日志

```bash
# 今天
./scripts/sync-daily.sh

# 指定日期
./scripts/sync-daily.sh 2026-02-18
```

### 晋升高价值记忆

```bash
./scripts/promote-to-memory-md.sh
```

## CortexGraph 工具

```bash
# 保存记忆
mcporter call cortexgraph.save_memory content="..." tags='["tag1"]'

# 搜索记忆
mcporter call cortexgraph.search_memory query="关键词"

# 强化记忆
mcporter call cortexgraph.touch_memory memory_id="UUID"

# 查看图谱
mcporter call cortexgraph.read_graph
```

## 架构

```
┌─────────────┐
│  MEMORY.md  │ ← 长期记忆（手动维护）
└──────┬──────┘
       │ sync
       ↓
┌─────────────┐
│ CortexGraph │ ← 智能层（自动衰减）
└──────┬──────┘
       │ sync
       ↓
┌─────────────┐
│  daily.log  │ ← 每日日志（自动导入）
└─────────────┘
```

## 配置

编辑 `~/.config/cortexgraph/.env`:

```env
CORTEXGRAPH_STORAGE_PATH=~/.config/cortexgraph/jsonl
CORTEXGRAPH_DECAY_MODEL=power_law
CORTEXGRAPH_PL_HALFLIFE_DAYS=3.0
CORTEXGRAPH_FORGET_THRESHOLD=0.05
CORTEXGRAPH_PROMOTE_THRESHOLD=0.65
```

## 许可证

MIT
