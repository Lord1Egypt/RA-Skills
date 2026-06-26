---
name: memory-tencentdb
description: 四层记忆系统插件 — 自动捕获对话、提取结构化记忆、归纳场景、生成用户画像。支持 L0→L1→L2→L3 渐进式管线，本地 SQLite + 腾讯云向量数据库双后端。
version: 0.3.8
tags: ["memory", "long-term-memory", "persona", "sqlite", "vector-search"]
author: paudyyin
---

# memory-tencentdb — 四层记忆系统

为 OpenClaw AI Agent 提供 L0→L1→L2→L3 长期记忆能力。

## v0.3.8 变更（2026-06-08）

- **集成 Nomic Atlas 可视化**：新增 `scripts/nomic_atlas_visualizer.py`，使用 sentence-transformers + nomic-embed-text-v1.5 生成 768 维语义嵌入，UMAP 降维后生成交互式 HTML 可视化，完全本地运行
- **删除 llm configSchema**：从 openclaw.plugin.json 中移除 `llm` 配置段（v0.3.7 已删除代码，此版本清理配置 schema）
- **本地 embedding 支持**：兼容 memorySearch.provider: "local" 配置，使用 nomic-embed-text-v1.5.Q4_K_M.gguf 本地模型
- **修复 L1 提取静默失败**：之前独立 LLM 因 apiKey 为空返回 401，导致提取管线完全停止

## v0.3.6 变更（2026-06-08）

- **移除独立 LLM 模式**：删除 `llm.enabled` 配置和 StandaloneLLMRunner，L1/L2/L3 提取统一走 Gateway 内置模型（runEmbeddedPiAgent）
- **简化配置**：不再需要单独配置 LLM API 端点和 Key，复用 Gateway 已有的模型认证
- **修复 L1 提取静默失败**：之前独立 LLM 因 apiKey 为空返回 401，导致提取管线完全停止

## 架构

```
对话开始
  → Auto-Recall: 向量/混合搜索相关记忆 + 加载 Persona → 注入系统上下文

对话结束
  → L0: 录制对话消息 → SQLite + JSONL 双写
  → Pipeline Scheduler: 达到 N 轮后触发
     ├── L1: LLM 提取结构化记忆 + 向量去重 → JSONL + SQLite
     ├── L2: LLM 归纳场景块 → Markdown 文件
     └── L3: LLM 生成/更新用户画像 → persona.md
```

## 四层记忆

| 层级 | 名称 | 说明 |
|------|------|------|
| L0 | 对话录制 | 原始对话消息捕获 |
| L1 | 记忆提取 | 结构化记忆（persona/episodic/instruction） |
| L2 | 场景归纳 | 场景块（Scene Block） |
| L3 | 用户画像 | 用户人格画像（Persona） |

## 记忆类型

- **persona**：用户的稳定属性、偏好、技能、价值观
- **episodic**：客观发生的动作、决定、计划或结果
- **instruction**：用户对 AI 的长期行为规则

## 安装

```bash
clawhub install memory-tencentdb
```

## 配置

在 openclaw.json 中添加：

```json
{
  "plugins": {
    "allow": ["mx", "memory-tencentdb"],
    "load": {
      "paths": ["<插件路径>"]
    },
    "entries": {
      "memory-tencentdb": {
        "enabled": true,
        "config": {
          "pipeline": {
            "everyNConversations": 3,
            "enableWarmup": true,
            "l1IdleTimeoutSeconds": 10
          }
        }
      }
    }
  }
}
```

> **注意**：v0.3.6 起不再需要 `llm` 配置段，L1/L2/L3 提取自动使用 Gateway 内置模型。

## 存储后端

- `sqlite`（默认）：本地 SQLite + sqlite-vec
- `tcvdb`：腾讯云向量数据库

## CLI 命令

```bash
openclaw memory-tdai seed --input conversations.json
```

## 故障排查

如果 L1 提取为空：
1. 检查 `plugins.allow` 包含 `"memory-tencentdb"`
2. 检查 `plugins.load.paths` 包含插件路径
3. 检查 Gateway 模型配置正常（`models.providers` 和 `agents.defaults.model`）
4. 检查 vectors.db 中 l1_fts 与 l1_records 行数一致
