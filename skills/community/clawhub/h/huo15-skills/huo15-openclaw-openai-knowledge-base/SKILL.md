---
name: huo15-openclaw-openai-knowledge-base
displayName: 火一五知识库技能
description: 火一五知识库技能 - 基于 Andrej Karpathy 的 LLM Knowledge Bases 方案。每个企微 Agent 独立隔离，自动在 Agent 工作目录下创建专属知识库。触发词：知识库、入库知识库、查询知识库、编译知识库、体检知识库、同步知识库、激活知识库。
homepage: https://github.com/zhaobod1/huo15-skills
metadata: { "openclaw": { "emoji": "📚", "requires": { "bins": ["obsidian-cli"] } } }
version: 2.2.1
dependencies:
  obsidian:
    description: 依赖 ClawHub obsidian 技能（vault 发现 + obsidian-cli 封装）。运行时自动使用。
    install: clawhub install obsidian --dir ~/.openclaw/workspace/skills
  obsidian-cli:
    description: Obsidian CLI 工具，用于 vault 发现和搜索。
    install: brew install yakitrak/yakitrak/obsidian-cli
safety:
  virus_total_note: 本技能不包含任何硬编码凭证。所有 API 凭据均从用户本机 OpenClaw 配置文件（models.json）运行时加载，代码中仅包含凭据引用逻辑。
---

# SKILL.md - huo15-knowledge-base

> 火一五知识库技能 - 基于 Andrej Karpathy 的 LLM Knowledge Bases 方案
> **每个企微 Agent 独立隔离**，自动在 Agent 工作目录下创建专属知识库

---

## 版本历史

- **v0.9.0** — Bug 修复（7项）、kb-lint 自动检查、元数据补全、文档改进
- **v0.8.0** — 新增 Obsidian 集成（wiki → vault 自动同步）
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
    ├── wiki/    → LLM 编译后的结构化百科（Obsidian 格式）
    └── cache/   → 临时缓存
                ↓
         Obsidian Vault（可选，自动同步）
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
| `kb-search` | 搜索知识库（含 Obsidian vault）|
| `kb-lint` | 体检知识库（自愈）|
| `kb-fetch` | 独立网页抓取工具 |
| `kb-llm.py` | LLM API 调用器 |
| `kb-sync` | **桥接 memory-evolution**（可选）|
| `obsidian-sync` | **同步 wiki 到 Obsidian vault** |

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
- "Obsidian 同步"、"同步到 Obsidian"

---

## Obsidian 集成（v0.8+）

编译后的 `wiki/` 会同步到 Obsidian vault，形成完整的**第二大脑**：

```
raw/ → LLM编译 → wiki/ → Obsidian Vault（知识库文件夹）
                              ↓
                    Obsidian 图谱视图 · 双向链接 · 搜索
```

### 配置（技能根目录 `config.json`）

```json
{
  "obsidian": {
    "enabled": true,
    "vault_path": "/Users/xxx/Documents/我的笔记"
  }
}
```

### Obsidian 同步命令

```bash
# 预览同步（不实际写入）
obsidian-sync.sh --dry-run

# 执行同步
obsidian-sync.sh

# 监听模式（wiki 变化自动同步）
obsidian-sync.sh --watch

# 启用+同步一步到位
obsidian-sync.sh --enable --vault '/path/to/vault'
```

### 搜索

`kb-search` 会同时搜索 wiki/ 和 Obsidian vault：
```bash
kb-search "Odoo ORM"
# → wiki/ 中找到 3 条
# → Obsidian vault 中找到 5 条
```

### Obsidian 效果

- 编译后的百科以 `知识库/` 文件夹出现在 vault 中
- 所有条目使用 `[[双向链接]]` 格式
- Obsidian 的**图谱视图**直接可视化知识网络
- 支持 `obsidian-cli` 管理（搜索/创建/移动笔记）

### 可选依赖

```bash
brew install obsidian-cli    # 安装 CLI（可选，不装也能文件同步）
```
