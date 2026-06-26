---
name: openviking-context
description: "OpenViking context database for AI agents — layered context loading (L0/L1/L2), semantic search, file-system memory management. Use when: (1) setting up OpenViking, managing agent memory/resources; (2) performing semantic search or browsing context filesystem; (3) comparing token consumption; (4) answering questions about project code, configs, components, or any knowledge base content by searching. Triggers on: 'openviking', 'context database', 'viking memory', 'layered context', 'token saving', 'L0/L1/L2', 'viking://', 'memsearch', 'memread', 'context setup', '知识库', '搜索.*项目', '查一下', '看一下', '帮我找', '搜索.*代码', '查看.*配置', '项目.*路径', '在哪', '怎么配置', '哪个文件', '哪个组件'."
---

# OpenViking Context Database

字节跳动开源的 Agent 上下文数据库。通过 `viking://` 文件系统协议统一管理记忆、资源和技能，L0/L1/L2 三层按需加载，token 消耗降低 83-96%。

| 能力 | 说明 |
|---|---|
| 文件系统协议 | `viking://` 统一管理 resources/user/agent 三类上下文 |
| L0/L1/L2 分层 | 摘要(~100 tokens) / 概览(~2k tokens) / 全文，按需加载 |
| 语义检索 | 目录递归检索 + 向量匹配 |
| 会话记忆 | 自动提取长期记忆，跨会话保持 |
| Token 节省 | 对比全量加载，输入 token 降低 83%~96% |

## 安装到 OpenClaw

```bash
bash scripts/install-skill.sh
```

脚本会将 skill 复制到 OpenClaw 的 skills 目录（自动检测路径），然后在 OpenClaw 中说 "refresh skills" 即可发现。

## 安装 OpenViking 依赖

skill 安装完成后，运行以下命令安装 OpenViking 本体：

```bash
bash scripts/install.sh
```

自动检测 Python >= 3.10，安装 `openviking` 包，创建工作目录，可选安装 Rust CLI (`ov`)。

## 配置

```bash
bash scripts/setup-config.sh
```

支持的模型提供商：

| 提供商 | VLM 模型 | Embedding 模型 |
|---|---|---|
| `openai` | gpt-4o | text-embedding-3-large (dim=3072) |
| `volcengine` | doubao-seed-2-0-pro-260215 | doubao-embedding-vision-250615 (dim=1024) |
| `litellm` | claude-3-5-sonnet / deepseek-chat | — |
| NVIDIA NIM | meta/llama-3.3-70b-instruct | nvidia/nv-embed-v1 (dim=4096) |

> **注意**：避免使用推理模型 (kimi-k2.5, deepseek-r1)，它们的 `reasoning` 字段与 OpenViking 不兼容。

## 第一次使用完整流程

首次安装时，按顺序执行以下步骤：

**Step 1 — 安装依赖**
```bash
bash ~/.openclaw/workspace/skills/openviking-token-saver/scripts/install.sh
```
> 自动检测 Python >= 3.10，创建 venv，安装 openviking 包

**Step 2 — 配置 API Key**
```bash
bash ~/.openclaw/workspace/skills/openviking-token-saver/scripts/setup-config.sh
```
> 交互式配置 VLM 和 Embedding 的 API Key、模型、API 地址

**Step 3 — 验证安装**
```bash
/Users/wuguanhua/.openviking/venv/bin/python3 ~/.openclaw/workspace/skills/openviking-token-saver/scripts/viking.py info
```
> 确认 ov.conf 配置正确，服务可连接

**Step 4 — 添加资源**
```bash
/Users/wuguanhua/.openviking/venv/bin/python3 ~/.openclaw/workspace/skills/openviking-token-saver/scripts/viking.py add ./你的项目文档路径/
```

**Step 5 — 开始搜索**
```bash
/Users/wuguanhua/.openviking/venv/bin/python3 ~/.openclaw/workspace/skills/openviking-token-saver/scripts/viking.py search "关键词"
```

> ⚠️ 所有 `viking.py` 命令都必须用 `~/.openviking/venv/bin/python3`，不能用系统 `python3`

## 启动服务器（可选）

`scripts/viking.py` 支持 **direct mode**（直接访问数据文件，不需要服务器）。服务器仅在使用 Web UI 时才需要。

```bash
# 启动 API 服务器（后台运行）
nohup ~/.openviking/venv/bin/openviking-server > ~/.openviking/server.log 2>&1 &

# 启动 Console Web UI（后台运行）
nohup ~/.openviking/venv/bin/python3 -m openviking.console.bootstrap \
  --host 127.0.0.1 --port 8020 \
  --openviking-url http://127.0.0.1:1933 \
  > ~/.openviking/console.log 2>&1 &

# API 文档地址
open http://localhost:1933/docs

# Console Web UI 地址
open http://localhost:8020
```

> **何时需要服务器：**
> - 需要 Web UI 管理界面 → 必须启动 API server + Console
> - 只需要 `scripts/viking.py` 做 search/add/read → **不需要**，direct mode 已够用

## 核心操作

通过 `scripts/viking.py` 与 OpenViking 交互（direct mode，不需要服务器）：

```bash
/Users/wuguanhua/.openviking/venv/bin/python3 scripts/viking.py <command> [args]
```

> ⚠️ **重要**：必须使用 venv 中的 Python（3.11），系统 Python 3.9 不支持 openviking。

| 命令 | 功能 | 示例 |
|---|---|---|
| `add <path_or_url>` | 添加资源（文件/URL/目录） | `viking.py add ./docs/` |
| `search <query>` | 语义搜索 | `viking.py search "认证逻辑"` |
| `ls [uri]` | 浏览资源目录 | `viking.py ls viking://resources/` |
| `tree [uri]` | 树形展示 | `viking.py tree viking://resources/ -L 2` |
| `abstract <uri>` | L0 摘要 (~100 tokens) | `viking.py abstract viking://resources/proj` |
| `overview <uri>` | L1 概览 (~2k tokens) | `viking.py overview viking://resources/proj` |
| `read <uri>` | L2 全文 | `viking.py read viking://resources/proj/api.md` |
| `info` | 检查服务状态 | `viking.py info` |
| `commit` | 提取当前会话记忆 | `viking.py commit` |
| `stats` | 查看 token 消耗统计 | `viking.py stats` |
| `stats --reset` | 重置统计数据 | `viking.py stats --reset` |

## Token 消耗追踪

每次调用 `search`、`abstract`、`overview`、`read` 时自动追踪：

- **实际消耗**：本次分层加载实际使用的 token 数
- **全量假设**：如果用传统方式全量加载同一资源需要的 token 数
- **节省量**：两者差值和百分比

每次命令结尾自动输出一行会话累计摘要：

```
📊 会话累计 | 实际: 2,300 tokens | 全量: 48,000 tokens | 节省: 45,700 (95.2%)
```

使用 `stats` 命令查看完整的逐操作明细表：

```bash
python3 scripts/viking.py stats
```

输出示例：

```
═══ Token 消耗统计 ═══
  会话开始: 2026-03-19 19:30:00
  操作次数: 4

  #    时间       操作       层级  实际     全量     节省     URI
  ──── ────────── ────────── ───── ──────── ──────── ──────── ──────────────────
  1    19:30:05   search     L0        300   48,000   47,700  用户认证 鉴权
  2    19:30:12   overview   L1      1,800   15,000   13,200  viking://resources/auth
  3    19:30:18   abstract   L0         80    8,000    7,920  viking://resources/db
  4    19:30:25   read       L2      3,200    3,200        0  viking://resources/auth/jwt

  ┌─────────────────────────────────────┐
  │  全量加载 (传统方式):     74,200 tokens │
  │  实际消耗 (分层加载):      5,380 tokens │
  │  节省 token 数量:        68,820 tokens │
  │  节省比例:                  92.8%        │
  └─────────────────────────────────────┘
```

统计数据持久化在 `~/.openviking/session_stats.json`，跨命令调用累积。新会话可用 `stats --reset` 重置。

## 分层加载工作流

收到开发需求（如"帮我写一个用户认证模块"）时：

**Step 1 — L0 快速扫描**（~300 tokens）

```bash
python3 scripts/viking.py search "用户认证 鉴权 登录"
```

用 L0 摘要判断哪些资源相关，过滤无关内容。

**Step 2 — L1 概览决策**（~2k tokens/资源）

```bash
python3 scripts/viking.py overview viking://resources/auth-docs
```

理解架构和技术选型，制定实现计划。

**Step 3 — L2 按需深读**（仅必要文件）

```bash
python3 scripts/viking.py read viking://resources/auth-docs/jwt-config.md
```

只加载写代码需要的具体文件。

### Token 对比演示

```bash
python3 scripts/demo-token-compare.py ./your-project-docs/
```

| 方案 | Token 消耗 | 说明 |
|---|---|---|
| 全量加载 (传统 RAG) | ~50,000 | 所有文档塞进 prompt |
| L0 扫描 + L1 概览 | ~3,000 | 分层按需，仅摘要和概览 |
| L0 + L1 + L2 按需 | ~8,000 | 最终只深读 2-3 个必要文件 |
| **节省比例** | **84%~94%** | 相比全量加载 |

## 故障排查

| 问题 | 原因 | 解决 |
|---|---|---|
| `Dense vector dimension mismatch` | embedding 维度配置错误 | 检查 ov.conf 中的 dimension 与模型匹配 |
| `NoneType is not subscriptable` | 使用了推理模型 | 换用 gpt-4o 或 llama-3.3-70b |
| `input_type required` | 使用了非对称 embedding | 换用对称模型如 nvidia/nv-embed-v1 |
| 搜索无结果 | 语义处理未完成 | 添加资源后等待：`viking.py add --wait` |
| 服务连接失败 | 服务器未启动 | 运行 `nohup ~/.openviking/venv/bin/openviking-server > ~/.openviking/server.log 2>&1 &` |
| `Embedding failed: No embedding data` | embedding API 调用失败 | 确认 ov.conf 中 key 有 embedding 权限；检查余额；确认模型名为 `embo-01` 且 provider 为 `openai` |
| `python3: command not found` 或 `No module named openviking` | 系统 Python 版本不对 | 必须用 `~/.openviking/venv/bin/python3`，不要用系统 python3 |

## 参考

- [OpenViking GitHub](https://github.com/volcengine/OpenViking)
- [OpenViking 官网](https://www.openviking.ai)
- [LiteLLM 提供商文档](https://docs.litellm.ai/docs/providers)
- [NVIDIA NIM API](https://build.nvidia.com/)
