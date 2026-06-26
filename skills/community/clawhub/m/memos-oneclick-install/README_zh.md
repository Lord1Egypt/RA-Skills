# MemOS for OpenClaw — 一键安装

> English version: [README.md](./README.md).

[![npm version](https://img.shields.io/npm/v/@memtensor/memos-local-openclaw-plugin)](https://www.npmjs.com/package/@memtensor/memos-local-openclaw-plugin)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/MemTensor/MemOS/blob/main/LICENSE)
[![Node.js >= 18](https://img.shields.io/badge/node-%3E%3D18-brightgreen)](https://nodejs.org/)
[![GitHub](https://img.shields.io/badge/GitHub-Source-181717?logo=github)](https://github.com/MemTensor/MemOS/tree/main/apps/memos-local-openclaw)

> [主页](https://memos-claw.openmem.net) · [文档](https://memos-claw.openmem.net/docs/) · [NPM](https://www.npmjs.com/package/@memtensor/memos-local-openclaw-plugin) · [故障排除](https://memos-claw.openmem.net/docs/troubleshooting.html)

---

## 本目录包含

| 文件 | 用途 |
| ---- | ---- |
| **`SKILL.md`** | 驱动一键安装的 Agent 技能。加载后，OpenClaw 读取此文件并 **自主** 完成 MemOS 插件的安装、配置与验证 —— 你只需回答一个问题。 |
| **`README.md` / 本文件** | 面向人类的总览：安装体验说明与 MemOS 功能介绍。 |

---

## 真正的一键安装：让 OpenClaw 替你完成

本目录中的 **`SKILL.md`** 不是一份手册 —— 它是一份 **机器可读的安装技能**，专为 OpenClaw Agent 设计。当你对 Agent 说出 *"安装 memos"* 或 *"install MemOS"*，以下流程会自动发生：

### 零手动操作

触发后，OpenClaw 执行一条 **6 步全自主流水线** —— 检测当前状态、安装插件、写入配置、重启网关、验证结果、交付最终总结。**你不需要自己执行任何命令。**

整个过程中唯一的交互只有一个问题：

> *选择嵌入模型 —— 本地离线模型 (A) 还是外部 API (B)？*

回复 `A` 或 `B`，其余一切由 OpenClaw 处理。如果是升级现有安装，连这个问题也会跳过 —— 全程无需干预。

### 自动识别操作系统 —— macOS、Linux、Windows 全适配

你无需告诉 Agent 你在用什么系统。技能通过 **`process.platform`**（`darwin` / `linux` / `win32`）自动检测操作系统，并据此调整每一条命令：

| 方面 | 如何适配 |
| ---- | -------- |
| **路径分隔符与主目录** | 所有路径通过 `require('path').join(...)` 和 `require('os').homedir()` 构建 —— 在每个系统上表现一致。 |
| **Shell 命令** | 主要方式为 `node -e "..."`，在 bash、PowerShell 和 cmd 中行为相同。仅在固有平台差异处（如 macOS/Linux 的 `nohup`、Windows 的 `Start-Process`）使用特定回退方案。 |
| **安装脚本回退** | 若 OpenClaw CLI 不可用，Agent 会根据系统自动选择 `install.sh`（macOS/Linux）或 `install.ps1`（Windows）—— 无需用户决定。 |
| **原生模块重编译** | `better-sqlite3` 会自动重编译以匹配本地 Node.js 版本；构建工具指引也是平台感知的（`xcode-select` / `apt install build-essential` / Visual Studio Build Tools）。 |

**一句话：** 无论你是用 Mac、Linux 服务器还是 Windows 工作站，说一声 *"安装 memos"*，然后坐等即可。

### 智能状态检测

技能不会盲目重装。在动手之前它会先检查：

- **未安装** —— 执行完整安装流水线（Steps 0 – 6）。
- **已安装但版本过旧** —— 自动升级，保留你现有的配置。
- **已是最新版本** —— 仅做快速验证；除非发现问题，否则不重启。
- **配置不完整或损坏** —— 自动修复，无需重新下载插件。

每个分支都由 Agent 自主判断。你永远不会被问到 *"你想做什么？"*。

---

## MemOS 带给你什么

安装完成后，MemOS 插件将 OpenClaw 变为一个 **具有记忆能力的 Agent** —— 100% 在本地设备上运行，默认使用本地嵌入模型时无需云端账号。

### 核心能力

| 能力 | 说明 |
| ---- | ---- |
| **持久记忆** | 每一轮对话自动采集、语义分块、嵌入并索引到本地 SQLite 数据库（`~/.openclaw/memos-local/memos.db`）。无需手动说"记住这个"。 |
| **混合检索** | FTS5 关键词搜索 + 向量语义搜索，通过倒数排名融合 (RRF) 与最大边际相关性 (MMR) 重排序。可配置的时间衰减偏向近期记忆。 |
| **任务总结** | 对话自动划分为任务。已完成任务生成结构化 LLM 摘要 —— 目标、关键步骤、结果，以及保留的代码/命令/URL/报错等关键细节。 |
| **技能演化** | 高质量任务执行被提炼为可复用技能（SKILL.md 格式），相似任务出现时可 **自动升级**。内建版本历史、质量评分和自动安装功能。 |
| **团队共享** | 可选 Hub–Client 架构：Hub 存储共享数据，Client 本地保留私密数据。支持范围检索（`local` / `group` / `all`）、任务共享、技能发布/拉取、管理员审批和实时通知。 |
| **Memory Viewer** | 本机 Web 仪表盘（默认 `http://127.0.0.1:18799`），共 7 个页面：记忆、任务、技能、分析、日志、导入、设置 —— 完整增删改查，中英文切换，明暗主题。 |
| **记忆迁移** | 一键导入 OpenClaw 原生内置记忆（SQLite + JSONL）至 MemOS，具有智能去重与断点续传功能。 |
| **多嵌入提供商** | 支持 OpenAI 兼容接口、Gemini、Cohere、Voyage、Mistral，或完全离线本地模型（`Xenova/all-MiniLM-L6-v2`）。 |

### 自动钩子 —— 无需手动「记住这句话」

| 钩子 | 触发时机 | 行为 |
| ---- | -------- | ---- |
| **`agent_end`** | 每轮结束后 | 消息被分块、嵌入、去重（内容哈希 + LLM 判断）并写入。 |
| **`before_agent_start`** | 每轮开始前 | 相关记忆注入上下文。若召回偏弱，Agent 会自动用自生成查询调用 `memory_search`。 |

### 可用工具

| 工具 | 作用 |
| ---- | ---- |
| `memory_search` | 关键词 + 语义检索记忆（支持范围）。 |
| `memory_get` / `memory_timeline` | 完整块文本 / 周边对话上下文。 |
| `memory_write_public` | 写入对所有本地 Agent 可见的共享记忆。 |
| `task_summary` | 已完成任务的结构化摘要。 |
| `skill_get` / `skill_search` / `skill_install` | 发现与安装演化出的技能。 |
| `memory_viewer` | 获取 Memory Viewer 访问地址。 |

还有 Hub–Client 网络工具（`task_share`、`skill_publish`、`network_skill_pull` 等）。完整参考见安装时自动部署的 **`memos-memory-guide`** 技能。

---

## 为何选择 MemOS —— 对比优势

| 痛点 | MemOS 如何解决 |
| ---- | -------------- |
| **Agent 跨会话失忆** | 持久化索引记忆 —— 每轮自动采集。 |
| **上下文浅、反复犯错** | 任务总结 + 技能演化，将原始聊天记录变为结构化、可复用的知识。 |
| **多 Agent 团队各自为战** | Hub–Client 共享，按范围检索、任务共享与技能发布 —— 私密数据仍留在本地。 |
| **看不到「它记住了什么」** | Memory Viewer：增删改查、分析、工具调用日志、迁移与在线配置集中于一处。 |
| **隐私与数据驻留顾虑** | 100% 本地优先 —— SQLite 在你的机器上。外部 API 可选，且仅在 **你** 配置后才使用。 |
| **系统兼容性** | 支持 macOS、Linux 和 Windows。安装技能自动识别系统并适配。 |
| **复杂的手动安装** | 一句话 —— *"安装 memos"* —— 触发全自主流水线。一个嵌入模型选择问题，零条需要你手动输入的命令。 |

MemOS 是更广泛的 [MemOS 记忆操作系统](../MemOS/README.md) 项目的一部分：面向 LLM 和 AI Agent 的统一存储/检索/管理平台，具有多模态记忆、知识库管理与企业级优化。本 OpenClaw 插件是其 **本地、设备端** 交付形态。

---

## 隐私与安全

- **100% 在设备上** —— 所有数据存于本地 SQLite，零云端上传。
- **匿名遥测** —— 可通过配置关闭；仅发送工具名称、延迟和版本信息，从不发送记忆内容、查询或个人数据。
- **Viewer 安全** —— 仅绑定 `127.0.0.1`，密码保护 + 会话 Cookie。

---

## 速查 —— 手动安装命令

多数情况下你只需说 *"安装 memos"*，让技能替你完成。如果你更倾向于自己执行：

**macOS / Linux：**

```bash
curl -fsSL https://cdn.memtensor.com.cn/memos-local-openclaw/install.sh | bash
```

**Windows（PowerShell）：**

```powershell
powershell -c "irm https://cdn.memtensor.com.cn/memos-local-openclaw/install.ps1 | iex"
```

**通过 OpenClaw CLI：**

```bash
openclaw plugins install @memtensor/memos-local-openclaw-plugin
```

然后配置 `~/.openclaw/openclaw.json`、启动网关并打开 Memory Viewer。详细选项、嵌入/总结模型对照表、团队共享与排错见[完整文档](https://memos-claw.openmem.net/docs/)。
