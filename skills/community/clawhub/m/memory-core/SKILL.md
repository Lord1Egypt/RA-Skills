---
name: memory-core
description: "OpenClaw 长期记忆核心：基于 LanceDB 的向量化长期记忆存储与检索，内置意图/场景隔离以防记忆污染。"
---

# Memory Core（长期记忆核心）

Memory Core 为 OpenClaw Agent 提供跨会话的长期记忆能力：自动识别输入的意图与场景，并在检索阶段进行严格场景隔离，避免无关记忆污染当前会话。

## 功能特性

- 记忆摄入：将用户关键事实写入长期记忆库
- 记忆检索：按 Agent + 场景过滤后进行向量相似度搜索
- 记忆遗忘：按记忆 ID 删除
- 本地优先：LanceDB 文件本地持久化，默认不出机器

## 命令

在 OpenClaw Workspace 内运行（`{baseDir}` 为技能目录）：

```bash
python3 {baseDir}/scripts/main.py ingest --agent "main" --text "我是 Python 后端工程师，喜欢用 FastAPI。"
python3 {baseDir}/scripts/main.py retrieve --agent "main" --query "我擅长什么框架？"
python3 {baseDir}/scripts/main.py forget --id "<memory_id>"
```

## 配置

你可以创建 `{baseDir}/config.json` 来选择本地或云端向量化模型：

### 预算自适应（推荐开启）

默认会根据 `agent_id` 在 `~/.openclaw/openclaw.json` 里对应的模型名做启发式分档，并自动选择检索预算：

- small：400/1200
- medium：600/1800
- large：900/2700

如需固定预算，可在 config.json 里设置 `auto_budget: false` 并手工指定 `max_chars_per_memory/max_total_chars`。

### 1) 使用本地 Ollama（推荐本地优先）

```json
{
  "embedding_provider": "ollama",
  "embedding_model": "nomic-embed-text",
  "embedding_base_url": "http://localhost:11434",
  "auto_budget": true,
  "default_tier": "medium",
  "embedding_timeout_sec": 20,
  "embedding_max_input_chars": 2000,
  "max_results": 5,
  "max_chars_per_memory": 600,
  "max_total_chars": 1800,
  "min_score": 0.2
}
```

### 2) 使用云端 SiliconFlow（默认）

`embedding_api_key` 可留空，系统会尝试从 `~/.openclaw/openclaw.json` 自动读取。

```json
{
  "embedding_provider": "siliconflow",
  "embedding_model": "BAAI/bge-m3",
  "embedding_base_url": "https://api.siliconflow.cn/v1",
  "auto_budget": true,
  "default_tier": "medium",
  "embedding_timeout_sec": 15,
  "embedding_max_input_chars": 2000,
  "max_results": 5,
  "max_chars_per_memory": 600,
  "max_total_chars": 1800,
  "min_score": 0.2
}
```
