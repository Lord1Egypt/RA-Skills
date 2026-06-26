---
name: memory-indexer
description: 短期记忆关键词索引工具 - 自动提取关键词、建立索引、搜索记忆，支持关联发现、时间线视图、重要记忆标记、三级级联搜索、会话备份与精简等功能。版本 2.0.0
homepage: https://github.com/smallmj/memory-indexer
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": ["python3"], "python_packages": ["jieba"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "packages": ["jieba"],
              "label": "Install jieba for Chinese word segmentation",
            },
          ],
      },
  }
---

# Memory Indexer 🧠

> 短期记忆关键词索引工具，为 AI Agent 提供长期记忆能力

**版本**: v2.0.0

## 简介

Memory Indexer 帮助 AI Agent 持久化记忆：

- 自动提取记忆中的关键词
- 建立关键词 → 记忆文件的快速索引
- 支持多关键词精确搜索（AND/OR 模式）
- 自动发现关联记忆
- 按时间线展示记忆
- 标记和查看重要记忆
- 增量同步外部记忆目录
- 会话备份与精简（避免 session memory 无限膨胀）

## 功能特性

1. 自动关键词提取：使用 jieba 中文分词
2. 多模式搜索：OR（任一匹配）/ AND（全部匹配）
3. 关联发现：自动发现经常一起出现的记忆
4. 时间线视图：按时间顺序展示记忆
5. 主动提醒：根据当前关键词提示相关旧记忆
6. 重要记忆标记：手动标记优先保留
7. 增量同步：只索引新增或修改的文件
8. 失效清理：自动清理已删除记忆的索引
9. **三级级联搜索**：关键词 → 向量语义 → 原文，自动降级
10. **向量语义搜索**：基于 HuggingFace bge-base-zh-v1.5 模型
11. **会话备份与精简**：备份用户消息到索引，精简 session 文件到 ~10KB
12. **Memory 文件精简**：备份 memory/*.md 到索引，精简大文件到 ~10KB
13. **新对话自动搜索**：Hook 机制，新会话开始时自动检索相关记忆
14. **压缩风险检测**：检测 memory 目录大小，评估压缩风险
15. **使用统计**：查看 memory 文件数量、大小、关键词统计
16. **快照备份**：压缩前自动/手动创建快照，支持恢复

## 安装

### 方式一：运行安装脚本（推荐）

```bash
git clone https://github.com/smallmj/memory-indexer.git
cd memory-indexer
chmod +x install.sh
./install.sh
```

### 方式二：手动安装

```bash
git clone https://github.com/smallmj/memory-indexer.git
cd memory-indexer
pip install -r requirements.txt
ln -sf "$(pwd)" ~/.openclaw/workspace/skills/memory-indexer
python3 memory-indexer.py status
```

## 快速开始

```bash
# 添加记忆
python memory-indexer.py add "今天学习了 Python"

# 搜索（OR 模式）
python memory-indexer.py search "Python"

# 搜索（AND 模式）
python memory-indexer.py search "Python 编程" --and

# 列出所有记忆
python memory-indexer.py list

# 记忆摘要
python memory-indexer.py summary
```

### 向量语义搜索（需要安装依赖）

```bash
# 安装向量模型依赖
pip install sentence-transformers

# 测试向量生成
python embedding.py test

# 查看向量索引状态
python embedding.py status

# 批量生成历史记忆的向量
python embedding.py reindex

# 三级级联搜索（默认）
python memory-indexer.py search "今天天气"
```

### Hook: 新对话自动搜索记忆

从 v2.0.0 开始，提供 OpenClaw Hook `memory-indexer-on-new`，在新对话开始时自动搜索相关记忆。

```bash
# 复制 Hook 目录到 OpenClaw
cp -r hooks/memory-indexer-on-new ~/.openclaw/hooks/

# 重启 Gateway 使其生效
openclaw gateway restart
```

## 命令参考

| 命令 | 功能 | 示例 |
|------|------|------|
| `add` | 添加记忆 | `add "今天学习了 Python"` |
| `search` | 搜索记忆 | `search "Python"` |
| `search --and` | AND 搜索 | `search "Python AI" --and` |
| `list` | 列出所有记忆 | `list` |
| `sync` | 同步外部目录 | `sync` |
| `cleanup` | 清理失效索引 | `cleanup` |
| `related` | 关联发现 | `related` |
| `timeline` | 时间线视图 | `timeline` |
| `recall` | 主动提醒 | `recall "Python"` |
| `summary` | 记忆摘要 | `summary` |
| `star` | 标记重要 | `star 20260312.md` |
| `stars` | 查看重要记忆 | `stars` |
| `status` | 查看状态 | `status` |

## 配置

数据目录：`~/.memory-indexer/`

```
~/.memory-indexer/
├── index.json          # 关键词索引
├── sync-state.json    # 同步状态
└── stars.json         # 重要记忆标记
```

## 依赖

- Python 3.8+
- jieba (中文分词)

## License

MIT
