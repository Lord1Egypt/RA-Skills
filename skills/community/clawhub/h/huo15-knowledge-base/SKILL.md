---
name: huo15-knowledge-base
displayName: 火一五知识库技能
description: 火一五知识库技能 - 基于 Andrej Karpathy 的 LLM Knowledge Bases 方案。每个企微 Agent 独立隔离，自动在 Agent 工作目录下创建专属知识库。触发词：知识库、入库知识库、查询知识库、编译知识库、体检知识库、同步知识库、激活知识库。
version: 0.7.2
dependencies: {}
---

# SKILL.md - huo15-knowledge-base

> 火一五知识库技能 - 基于 Andrej Karpathy 的 LLM Knowledge Bases 方案
> **每个企微 Agent 独立隔离**，自动在 Agent 工作目录下创建专属知识库

---

## 版本历史

- **v0.5.0** — Phase 5: 桥接 memory-evolution（可选）
- v0.4.0 — Phase 4: LLM 编译自动化
- v0.3.0 — Phase 3: 自动抓取功能
- v0.2.0 — Agent 隔离架构
- v0.1.0 — 初始设计

---

## 核心概念

```
共享 Skill 代码（~/.openclaw/workspace/skills/huo15-knowledge-base/）
                ↓
每个 Agent 独立的数据目录（~/.openclaw/agents/{agent-id}/agent/kb/）
    ├── raw/     → 原始文档（按日期分目录）
    ├── wiki/    → LLM 编译后的结构化百科
    └── cache/   → 临时缓存
```

---

## 快速开始

### 独立使用（无需 memory-evolution）
```bash
kb-ingest --url "https://..."   # 入库 + 自动抓取
kb-compile                        # LLM 自动编译
kb-search "关键词"                 # 搜索
kb-lint                           # 体检
```

### 配合 memory-evolution 使用
```bash
kb-sync                           # 同步 reference 记忆到知识库
kb-compile                        # 编译同步的记忆
kb-search "Claude Code"           # 搜索共享知识
```

---

## 核心脚本

| 脚本 | 功能 |
|------|------|
| `kb-ingest` | 入库文档（自动抓取网页内容）|
| `kb-compile` | LLM 自动编译 raw → wiki |
| `kb-search` | 搜索知识库 |
| `kb-lint` | 体检知识库（自愈）|
| `kb-fetch` | 独立网页抓取工具 |
| `kb-llm.py` | LLM API 调用器 |
| `kb-sync` | **桥接 memory-evolution**（可选）|

---

## Phase 5: 桥接 memory-evolution（可选）

**设计原则：独立运行，不强制依赖**

```
kb-sync 检测 memory-evolution 存在?
    │
    ├── YES → 同步 reference 记忆到 kb/raw/_memory-reference/
    │         kb-compile 编译成 wiki 条目
    │         知识库可搜索 Claude Code、系统指针等 reference
    │
    └── NO → standalone 模式，跳过同步
             知识库正常独立运行
```

**kb-sync 命令：**
```bash
kb-sync                  # 同步 reference → 知识库（默认）
kb-sync --from-memory   # 同上
kb-sync --to-memory      # 暂不支持（单向桥接）
```

**同步内容：**
- `memory/reference/` 下的所有 .md 文件
- 包括：Claude Code 规范、系统指针、项目参考等
- 保存到 `kb/raw/_memory-reference/`

**搜索示例：**
```bash
kb-search "Claude Code"   # 搜到 Claude Code 记忆规范参考
kb-search "GitHub"        # 搜到 GitHub 相关 reference
```

---

## Agent 隔离架构

**设计原则：**
- Skill 代码共享，不重复安装
- 数据目录在每个 Agent 的 `agent/kb/` 下，完全隔离
- 通过 `AGENT_DIR` 环境变量自动检测当前 Agent 上下文

---

## 触发词

- "知识库"、"入库知识库"、"查询知识库"
- "编译知识库"、"体检知识库"、"同步知识库"
- "激活知识库"

---

## 配置

Agent 专属配置：`~/.openclaw/agents/{agent-id}/agent/kb/config.json`

```json
{
  "version": "0.5.0",
  "agent_context": "...",
  "paths": {
    "raw": "raw",
    "wiki": "wiki",
    "cache": "cache"
  },
  "memory_bridge": {
    "enabled": true,
    "auto_sync": false
  }
}
```
