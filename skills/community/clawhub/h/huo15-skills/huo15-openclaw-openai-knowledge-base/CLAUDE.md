# CLAUDE.md

**项目：huo15-knowledge-base** — LLM 驱动的结构化知识库

## 背景

基于 Andrej Karpathy 的 LLM Knowledge Bases 方案：
- 用 LLM 作为"研究图书馆员"，主动编译和维护 Markdown 知识库
- 绕过传统 RAG 的向量数据库，用人类可读的 Wiki 代替黑盒 embedding
- 核心创新：**Compilation Step** — LLM 读取 raw/ 原始文档，生成结构化 wiki

## 架构

```
raw/   → 原始文档入库（按日期分目录）
wiki/  → LLM 编译后的百科全书（Markdown）
cache/ → 临时缓存
```

**Agent 隔离**: 每个企微 Agent 的数据存在 `~/.openclaw/agents/{agent-id}/agent/kb/`，技能代码共享。

## 脚本体系

本技能有两套脚本，开发时请注意区分：

### 主脚本（kb-* 前缀，推荐使用）
| 脚本 | 作用 |
|------|------|
| `kb-ingest` | 文档入库（支持 URL/文件/文本，自动抓取）|
| `kb-compile` | 编译 raw → wiki（调用 LLM）|
| `kb-search` | 搜索 wiki + Obsidian vault |
| `kb-lint` | 自动体检 + 可选 LLM 深度分析 |
| `kb-fetch` | 独立网页抓取工具（纯 Python stdlib）|
| `kb-llm.py` | LLM API 调用器（从 models.json 加载凭证）|
| `kb-sync` | 桥接 memory-evolution（可选）|

### 辅助脚本
| 脚本 | 作用 |
|------|------|
| `activate.sh` | 为 Agent 初始化 kb/ 数据目录 |
| `env.sh` | 加载环境变量（source 使用）|
| `obsidian-sync.sh` | 同步 wiki → Obsidian vault |
| `init.sh` | 已弃用，转发到 activate.sh |

### 遗留脚本（*.sh，保留兼容）
`compile.sh`、`ingest.sh`、`search.sh`、`lint.sh`、`index.sh` — 这些是 Agent 隔离架构之前的版本，操作技能源码目录而非 Agent 数据目录。保留以兼容旧工作流，新开发请使用 kb-* 脚本。

## 配置加载链路

```
~/.openclaw/agents/{agent-id}/agent/models.json   → LLM 凭证（provider, apiKey）
技能目录/config.json                                → 技能配置（Obsidian, 编译参数）
环境变量 AGENT_DIR                                   → Agent 上下文检测
```

- `models.json` 由 OpenClaw 运行时管理，代码中不硬编码凭证
- `config.json` 从 `config.example.json` 复制生成
- 所有 kb-* 脚本通过 `AGENT_DIR` 定位数据目录，默认 `~/.openclaw/agents/main/agent`

## 开发规范

- 所有数据存 Markdown，纯文本友好
- LLM 调用通过 OpenClaw API，不硬编码模型
- 配置通过 `config.json`，敏感信息不上传
- 与 memory-evolution 通过 `memory/reference/` 类型桥接
- Python 脚本仅用标准库（urllib, html.parser, json, re），无第三方依赖

## 已知局限

- `kb-compile` 的 prompt 大小受 LLM token 限制，大量文档需分批
- Obsidian CLI 为可选依赖，未安装时降级为 grep 搜索
- `kb-sync --to-memory` 方向暂未实现（单向桥接）
- 遗留 *.sh 脚本的路径仍指向技能源码目录，不适用于 Agent 隔离场景
