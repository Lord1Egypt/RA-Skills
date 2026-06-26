---
name: personal-memory-system
version: 1.0.0
description: >
  一个自动化、双层记忆系统，用于持久化和可查询个人知识。它将用户在 MEMORY.md 中的长期记忆，自动同步到 SQLite 数据库 memory.db，实现“自然语言 → SQL 查询”的智能检索。

  **使用场景**：
  (1) 用户需要查询“我过去对 AI 模型的看法？”
  (2) 用户希望系统自动记录重要决策，避免“心理笔记”
  (3) 需要一个可版本控制、可检索的个人知识库

  **核心功能**：
  - 自动将 MEMORY.md 中的 ### 标题块同步到 memory.db 数据库
  - 支持通过自然语言提问，系统自动执行 SQL 查询
  - 与 Obsidian 和 Git 同步，实现个人知识库的完整闭环

  **系统依赖**：
  - 必须存在 /home/awu/.openclaw/workspace-work/MEMORY.md
  - 必须存在 /home/awu/.openclaw/workspace-work/auto_sync_memory.py
  - 必须存在 /home/awu/.openclaw/workspace-work/memory.db

  **重要**：此技能不提供任何外部 API 调用，所有数据均存储在本地，安全可靠。
---
# Personal Memory System

## 概述

这是一个为 OpenClaw 设计的个人知识管理技能。它解决了“人类记忆不可靠”的核心问题，通过自动化流程，将你最重要的想法和决策从易遗忘的 Markdown 文本，转化为机器可查询的结构化数据库。

## 工作原理

1. **输入**：你将重要的洞察、决策、经验写入 `/home/awu/.openclaw/workspace-work/MEMORY.md` 文件，使用 `###` 标题分隔不同主题。
2. **同步**：每当 OpenClaw 的心跳（heartbeat）被触发，`auto_sync_memory.py` 脚本会自动运行。
3. **处理**：脚本读取 `MEMORY.md`，将每个 `###` 标题及其下的内容解析为一条数据库记录。
4. **输出**：这些记录被写入 `/home/awu/.openclaw/workspace-work/memory.db` SQLite 数据库。
5. **查询**：当你提出自然语言问题（如“我过去对 AI 模型的看法？”），AI 助手会将问题转换为 SQL 查询（`SELECT content FROM memories WHERE content LIKE '%AI%'`），从 `memory.db` 中精准检索出所有相关记忆，并为你总结。

## 系统组件

- `MEMORY.md`：你的个人长期记忆库，人类可读，可版本控制。
- `memory.db`：自动同步的 SQLite 数据库，机器可查询。
- `auto_sync_memory.py`：核心同步脚本，由 OpenClaw 心跳机制调用。

## 安装与使用

1. **安装**：将此技能包放入 OpenClaw 的 `skills` 目录，或通过 `clawhub install personal-memory-system` 安装。
2. **初始化**：确保你的工作区根目录下存在 `MEMORY.md` 文件。如果不存在，请创建它。
3. **运行**：无需手动操作。系统会在每次心跳时自动同步。
4. **查询**：直接向 AI 助手提问，例如：“我过去对 Obsidian 的看法是什么？” 系统会自动检索并回答。

## 安全与隐私

- **完全本地化**：所有数据（`MEMORY.md`, `memory.db`）均存储在你的本地工作区，不上传、不共享。
- **无外部依赖**：不调用任何网络 API，不访问云服务。
- **可审计**：所有操作均在你的控制之下，你可以随时查看 `MEMORY.md` 和 `memory.db` 的内容。

## 未来扩展

- 与 Obsidian 的双向链接功能集成，自动生成知识图谱。
- 每日自动生成 `memory/YYYY-MM-DD.md` 的摘要。
- 支持导出 `memory.db` 为 CSV 或 JSON 以供备份。

> **“记忆不是用来记住的，是用来被访问的。”**
> —— 你的数字大脑
