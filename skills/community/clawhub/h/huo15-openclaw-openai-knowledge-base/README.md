# huo15-knowledge-base

> 基于 Andrej Karpathy LLM Knowledge Bases 方案，让 LLM 成为你的"研究图书馆员"
> **v0.8+ 支持 Obsidian 集成**，编译后自动同步到 vault，形成第二大脑

## 核心理念

传统 RAG 方案：文档 → 分块 → 向量数据库 → 相似性检索 → LLM

Karpathy 方案：原始文档 → LLM 主动编译 → 结构化 Markdown Wiki → LLM 直接阅读

**区别：AI 不是在"检索"，而是在"查阅百科全书"**

## 完整工作流

```
kb-ingest --url "https://..."   入库 + 抓取
        ↓
     raw/（按日期归档）
        ↓
kb-compile                     LLM 编译
        ↓
     wiki/（结构化百科）
        ↓
obsidian-sync                  自动同步
        ↓
Obsidian vault「知识库/」
        ↓
   图谱视图 · 双向链接 · 搜索
```

## 快速开始

```bash
# 1. 入库文档
kb-ingest --url "https://www.odoo.com/documentation/19.0/zh_CN/applications.html"

# 2. 编译 + 自动同步到 Obsidian
kb-compile

# 3. 搜索（wiki/ + Obsidian vault）
kb-search "Odoo ORM"

# 4. 体检知识库
kb-lint
```

## 核心命令

| 命令 | 说明 |
|------|------|
| `kb-ingest --url "..."` | 入库网页（自动抓取内容）|
| `kb-ingest --file /path/to/file` | 入库本地文件（PDF、RST、TXT）|
| `kb-ingest --text "内容"` | 直接输入文本入库 |
| `kb-compile [--incremental]` | LLM 编译 + 自动 Obsidian 同步 |
| `kb-search "关键词"` | 搜索 wiki/ + Obsidian vault |
| `kb-lint` | 体检知识库（自愈）|
| `kb-sync` | 同步 memory-evolution 记忆到知识库 |
| `obsidian-sync [--watch]` | 手动同步 wiki/ 到 Obsidian vault |

## Obsidian 集成

编译后的 wiki/ 会自动同步到 Obsidian vault 的 `知识库/` 目录。

**配置**（`config.json`）：
```json
{
  "obsidian": {
    "enabled": true,
    "vault_path": "/Users/xxx/Documents/我的笔记"
  }
}
```

**效果**：
- Obsidian **图谱视图**直接可视化知识网络
- `[[双向链接]]` 自动关联相关条目
- `obsidian-cli search` 加速搜索

## 目录结构

```
知识库数据目录（~/.openclaw/agents/{agent-id}/agent/kb/）
├── raw/          原始资料（按日期分目录）
├── wiki/         LLM 编译后的百科全书（Obsidian 格式）
└── cache/        临时缓存

Obsidian Vault/
└── 知识库/       编译后的百科（obsidian-sync 自动同步）
```

## 与记忆系统的区别

| | huo15-memory-evolution | huo15-knowledge-base |
|--|---|---|
| 本质 | Agent 的"记忆" | 外部知识的"图书馆" |
| 内容 | 决策、偏好、上下文 | 论文、文档、百科 |
| 维护 | 自己维护自己 | LLM 整理维护 |
| 可审计 | 是 | 是（人类可读 Markdown）|
| Obsidian | — | ✅ 图谱视图 + 双向链接 |

## License

MIT
