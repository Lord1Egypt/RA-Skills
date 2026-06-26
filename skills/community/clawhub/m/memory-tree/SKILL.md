---
name: memory-tree
description: 🌳 记忆树 — 周报自动生成，永久记忆标记，关键词搜索。说句话就能用。
---

# 🌳 记忆树

让 OpenClaw 拥有人类般的记忆——记住重要的，忘记过期的。

## 核心功能

| 功能 | 命令 |
|------|------|
| 生成周报 | `python3 scripts/memory_tree.py weekly` |
| 搜索记忆 | `python3 scripts/memory_tree.py search "关键词"` |
| 标记永久 | `python3 scripts/memory_tree.py mark "标题"` |

## 一句话使用

- 「生成周报」— 自动统计本周新记、遗忘、永久记忆
- 「搜索记忆 关键词」— 本地关键词搜索
- 「记住这个」— 标记为永久记忆 📌

## 特点

- **零依赖**：无需 Ollama，纯本地运行
- **自动推送**：周报自动检测已启用的渠道（飞书等）
- **永久记忆**：📌 标记永不衰减

## 安装

```bash
clawhub install memory-tree
```

## License

MIT
